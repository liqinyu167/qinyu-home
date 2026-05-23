import json
import os
import asyncio
import time
import logging
import shutil
import re
from pathlib import Path
from typing import Any, Optional
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

# ─── Config ───────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
SITES_FILE = DATA_DIR / "sites.json"
MODELS_FILE = DATA_DIR / "models.json"
CLICKS_LOG = DATA_DIR / "clicks.log"
CLICKS_CACHE = DATA_DIR / "clicks.json"
ADMIN_KEY = os.environ.get("ADMIN_API_KEY", "")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("aigc-api")

# ─── Global State ─────────────────────────────────────────────────────
nav_data: dict[str, Any] = {}        # full sites.json content
clicks: dict[str, int] = {}          # site_id -> total clicks
_last_click_flush: float = time.time()
CLICK_FLUSH_INTERVAL: int = 300      # 5 min flush to disk
write_lock = asyncio.Lock()
_hot_reload_disabled: bool = False   # prevents watchdog echo when CRUD writes


# ─── Auth Dependency ─────────────────────────────────────────────────
async def require_admin(authorization: str = Header("")):
    if not ADMIN_KEY:
        return True
    token = authorization.removeprefix("Bearer ").strip()
    if token != ADMIN_KEY:
        raise HTTPException(403, "Invalid admin key")
    return True


# ─── Atomic File Write ───────────────────────────────────────────────
def atomic_write(data: Any, path: Path) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    tmp.replace(path)


# ─── Data Loading ────────────────────────────────────────────────────
def load_data() -> None:
    global nav_data
    # Load sites (categories + sites)
    if SITES_FILE.exists():
        nav_data = json.loads(SITES_FILE.read_text(encoding="utf-8"))
    else:
        nav_data = {"categories": [], "sites": []}
    # Merge models from separate file
    if MODELS_FILE.exists():
        models_data = json.loads(MODELS_FILE.read_text(encoding="utf-8"))
        nav_data["models"] = models_data.get("models", [])
        if "models_updated" in models_data:
            nav_data["models_updated"] = models_data["models_updated"]
    else:
        nav_data.setdefault("models", [])
    logger.info(f"data loaded: {len(nav_data.get('sites', []))} sites, {len(nav_data.get('models', []))} models")


def load_clicks() -> None:
    """Recover clicks from cache, then replay log."""
    global clicks
    clicks = {}
    if CLICKS_CACHE.exists():
        clicks.update(json.loads(CLICKS_CACHE.read_text(encoding="utf-8")))
    if CLICKS_LOG.exists():
        for line in CLICKS_LOG.read_text(encoding="utf-8").strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
                clicks[item["site_id"]] = clicks.get(item["site_id"], 0) + 1
            except Exception:
                continue
    logger.info(f"clicks recovered: {len(clicks)} items, {sum(clicks.values())} total")


async def flush_clicks() -> None:
    """Periodic flush of clicks dict to cache file, then truncate log."""
    global _last_click_flush
    try:
        async with write_lock:
            atomic_write(clicks, CLICKS_CACHE)
            # Truncate log after flush to prevent double-count on restart
            CLICKS_LOG.write_text("")
        _last_click_flush = time.time()
        logger.debug(f"clicks flushed ({sum(clicks.values())} total)")
    except Exception as e:
        logger.error(f"clicks flush failed: {e}")


# ─── Watchdog Hot Reload ─────────────────────────────────────────────
class DataFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if _hot_reload_disabled:
            return
        if event.src_path and (event.src_path.endswith("sites.json") or event.src_path.endswith("models.json")):
            asyncio.run(_hot_reload())


async def _hot_reload():
    global _hot_reload_disabled
    if _hot_reload_disabled:
        return
    async with write_lock:
        try:
            load_data()
            logger.info("♻️  data/*.json 热更新完成")
        except Exception as e:
            logger.error(f"热更新失败: {e}")


# ─── Helper Functions ────────────────────────────────────────────────
def category_lookup(categories: list[dict]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for group in categories:
        lookup[group.get("id", "")] = group.get("label", "")
        for child in group.get("children", []):
            lookup[child.get("id", "")] = child.get("label", "")
    return lookup


def enrich_site(site: dict, labels: dict[str, str]) -> dict:
    primary = site.get("primarySection", "")
    return {
        **site,
        "primarySectionLabel": labels.get(primary, primary),
        "sectionLabels": [labels.get(s, s) for s in site.get("sections", [])],
    }


def get_filtered_sites(
    q: str = "", section: str = "", tag: str = ""
) -> list[dict]:
    labels = category_lookup(nav_data.get("categories", []))
    sites = [enrich_site(s, labels) for s in nav_data.get("sites", [])]

    keyword = q.strip().lower()
    if keyword:
        sites = [
            s for s in sites
            if keyword in " ".join([
                s.get("name", ""), s.get("description", ""),
                " ".join(s.get("tags", [])),
                " ".join(s.get("capabilities", [])),
            ]).lower()
        ]
    if section:
        sites = [s for s in sites if section in s.get("sections", [])]
    if tag:
        sites = [s for s in sites if tag in s.get("tags", [])]
    sites.sort(key=lambda site: (-int(site.get("weight") or 0), site.get("name", "").lower()))
    return sites


class SitePayload(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=1)
    url: str = Field(min_length=1)
    description: str = ""
    type: str = "tool"
    weight: int = 0
    primarySection: str = ""
    sections: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    relations: dict[str, list[str]] = Field(default_factory=dict)
    icon: Optional[str] = None


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or f"site-{int(time.time())}"


def unique_site_id(base_id: str, current_id: Optional[str] = None) -> str:
    existing = {
        site.get("id")
        for site in nav_data.get("sites", [])
        if site.get("id") != current_id
    }
    candidate = slugify(base_id)
    if candidate not in existing:
        return candidate
    index = 2
    while f"{candidate}-{index}" in existing:
        index += 1
    return f"{candidate}-{index}"


def normalize_site(payload: SitePayload, current_id: Optional[str] = None, previous: Optional[dict] = None) -> dict:
    data = payload.model_dump()
    name = data["name"].strip()
    url = data["url"].strip()
    if not name:
        raise HTTPException(400, "name is required")
    if not url.startswith(("http://", "https://")):
        raise HTTPException(400, "url must start with http:// or https://")

    site_id = current_id or data.get("id") or slugify(name)
    site_id = unique_site_id(site_id, current_id=current_id)

    sections = [item.strip() for item in data.get("sections", []) if item.strip()]
    primary = data.get("primarySection", "").strip()
    if primary and primary not in sections:
        sections.insert(0, primary)

    normalized = {
        **(previous or {}),
        **data,
        "id": site_id,
        "name": name,
        "url": url,
        "description": data.get("description", "").strip(),
        "type": data.get("type", "tool").strip() or "tool",
        "weight": int(data.get("weight") or 0),
        "primarySection": primary,
        "sections": sections,
        "capabilities": sorted({item.strip() for item in data.get("capabilities", []) if item.strip()}),
        "tags": [item.strip() for item in data.get("tags", []) if item.strip()],
        "relations": data.get("relations") or (previous or {}).get("relations", {}),
    }
    return normalized


def persist_nav_data() -> None:
    global _hot_reload_disabled
    _hot_reload_disabled = True
    try:
        # Only write sites-related data to sites.json (categories + sites)
        sites_only = {k: nav_data[k] for k in ["categories", "sites"] if k in nav_data}
        atomic_write(sites_only, SITES_FILE)
    finally:
        _hot_reload_disabled = False


# ─── Application Lifespan ────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    load_data()
    load_clicks()

    observer = PollingObserver()
    observer.schedule(DataFileHandler(), str(DATA_DIR), recursive=False)
    observer.start()
    logger.info("watchdog 文件监听已启动 (data/)")

    async def click_flusher():
        while True:
            await asyncio.sleep(60)
            if time.time() - _last_click_flush >= CLICK_FLUSH_INTERVAL:
                await flush_clicks()

    flusher_task = asyncio.create_task(click_flusher())

    yield

    # Shutdown
    observer.stop()
    observer.join()
    await flush_clicks()
    flusher_task.cancel()
    logger.info("API 已优雅关闭")


# ─── FastAPI App ─────────────────────────────────────────────────────
app = FastAPI(
    title="白刀的 AIGC 工具箱 API",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=str(ROOT_DIR / "assets")), name="assets")


# ═══════════════════════════════════════════════════════════════════════
#  READ APIs (existing, enhanced)
# ═══════════════════════════════════════════════════════════════════════

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "2.0", "message": "AIGC 工具箱 API 运行中"}


@app.get("/api/sites")
async def get_sites(q: str = "", section: str = "", tag: str = ""):
    sites = get_filtered_sites(q, section, tag)
    return {
        "categories": nav_data.get("categories", []),
        "sites": sites,
        "models": nav_data.get("models", []),
        "total": len(sites),
    }


@app.get("/api/models")
async def get_models(category: str = ""):
    models = nav_data.get("models", [])
    if category:
        models = [m for m in models if m.get("category") == category]
    return {"models": models, "total": len(models)}


@app.get("/api/categories")
async def get_categories():
    return {"categories": nav_data.get("categories", [])}


@app.get("/api/tags")
async def get_tags():
    tags = sorted({
        tag for site in nav_data.get("sites", [])
        for tag in site.get("tags", [])
    })
    return {"tags": tags}


@app.get("/api/stats")
async def get_stats():
    sites = nav_data.get("sites", [])
    labels = category_lookup(nav_data.get("categories", []))
    sections: dict[str, int] = {}
    for site in sites:
        key = site.get("primarySection") or "uncategorized"
        sections[key] = sections.get(key, 0) + 1
    return {
        "total": len(sites),
        "sections": [
            {"id": k, "name": labels.get(k, k), "count": c}
            for k, c in sorted(sections.items(), key=lambda x: -x[1])
        ],
        "tags": len({t for s in sites for t in s.get("tags", [])}),
        "capabilities": len({c for s in sites for c in s.get("capabilities", [])}),
        "totalClicks": sum(clicks.values()),
        "clicks": dict(sorted(clicks.items(), key=lambda x: -x[1])[:20]),
    }


@app.get("/api/sites/{site_id}")
async def get_site(site_id: str):
    for site in nav_data.get("sites", []):
        if site.get("id") == site_id:
            labels = category_lookup(nav_data.get("categories", []))
            return enrich_site(site, labels)
    raise HTTPException(404, f"Site '{site_id}' not found")


@app.get("/api/clicks/{site_id}")
async def get_site_clicks(site_id: str):
    return {"site_id": site_id, "clicks": clicks.get(site_id, 0)}


@app.get("/api/clicks/top")
async def get_top_clicks(limit: int = 20):
    sorted_clicks = sorted(clicks.items(), key=lambda x: -x[1])[:limit]
    sites_map = {s["id"]: s["name"] for s in nav_data.get("sites", [])}
    return {
        "top": [
            {"site_id": sid, "name": sites_map.get(sid, sid), "clicks": c}
            for sid, c in sorted_clicks
        ]
    }


# ═══════════════════════════════════════════════════════════════════════
#  CLICK TRACKING
# ═══════════════════════════════════════════════════════════════════════

@app.post("/api/track/click")
async def track_click(site_id: str):
    clicks[site_id] = clicks.get(site_id, 0) + 1
    # Append to log (non-blocking, best-effort)
    try:
        line = json.dumps({"site_id": site_id, "ts": datetime.utcnow().isoformat()})
        CLICKS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(CLICKS_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        logger.warning(f"click log append failed: {e}")
    return {"ok": True}


# ═══════════════════════════════════════════════════════════════════════
#  CRUD APIs (admin only)
# ═══════════════════════════════════════════════════════════════════════

@app.get("/api/admin/sites")
async def admin_sites(q: str = "", _=Depends(require_admin)):
    return await get_sites(q=q)


@app.post("/api/admin/sites")
async def create_site(payload: SitePayload, _=Depends(require_admin)):
    async with write_lock:
        site = normalize_site(payload)
        nav_data.setdefault("sites", []).append(site)
        persist_nav_data()
    logger.info(f"site created: {site['id']}")
    return {"status": "ok", "site": enrich_site(site, category_lookup(nav_data.get("categories", [])))}


@app.put("/api/admin/sites/{site_id}")
async def update_site(site_id: str, payload: SitePayload, _=Depends(require_admin)):
    async with write_lock:
        sites = nav_data.get("sites", [])
        for i, site in enumerate(sites):
            if site.get("id") == site_id:
                updated = normalize_site(payload, current_id=site_id, previous=site)
                sites[i] = updated
                persist_nav_data()
                logger.info(f"site updated: {site_id}")
                return {"status": "ok", "site": enrich_site(updated, category_lookup(nav_data.get("categories", [])))}
    raise HTTPException(404, f"Site '{site_id}' not found")


@app.delete("/api/admin/sites/{site_id}")
async def delete_site(site_id: str, _=Depends(require_admin)):
    async with write_lock:
        sites = nav_data.get("sites", [])
        new_sites = [s for s in sites if s.get("id") != site_id]
        if len(new_sites) == len(sites):
            raise HTTPException(404, f"Site '{site_id}' not found")
        nav_data["sites"] = new_sites
        persist_nav_data()
    logger.info(f"site deleted: {site_id}")
    return {"status": "ok", "id": site_id}


@app.post("/api/admin/reload")
async def admin_reload(_=Depends(require_admin)):
    """Force reload data files from disk."""
    await _hot_reload()
    return {"status": "ok", "sites": len(nav_data.get("sites", [])), "models": len(nav_data.get("models", []))}
