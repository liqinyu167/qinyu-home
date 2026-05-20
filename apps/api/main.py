import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="白刀的 AIGC 工具箱 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = ROOT_DIR / "data" / "sites.json"


def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {"categories": [], "sites": []}
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))


def category_lookup(categories: list[dict[str, Any]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for group in categories:
        lookup[group.get("id", "")] = group.get("label", "")
        for child in group.get("children", []):
            lookup[child.get("id", "")] = child.get("label", "")
    return lookup


def enrich_site(site: dict[str, Any], labels: dict[str, str]) -> dict[str, Any]:
    primary_section = site.get("primarySection", "")
    return {
        **site,
        "primarySectionLabel": labels.get(primary_section, primary_section),
        "sectionLabels": [labels.get(section, section) for section in site.get("sections", [])],
    }


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "AIGC 工具箱 API 运行中"}


@app.get("/api/sites")
async def get_sites(
    q: str = Query("", description="搜索关键词"),
    section: str = Query("", description="分类 ID"),
    tag: str = Query("", description="标签"),
):
    data = load_data()
    labels = category_lookup(data.get("categories", []))
    sites = [enrich_site(site, labels) for site in data.get("sites", [])]

    keyword = q.strip().lower()
    if keyword:
        sites = [
            site for site in sites
            if keyword in " ".join([
                site.get("name", ""),
                site.get("description", ""),
                " ".join(site.get("tags", [])),
                " ".join(site.get("capabilities", [])),
            ]).lower()
        ]

    if section:
        sites = [site for site in sites if section in site.get("sections", [])]

    if tag:
        sites = [site for site in sites if tag in site.get("tags", [])]

    return {"categories": data.get("categories", []), "sites": sites}


@app.get("/api/categories")
async def get_categories():
    return {"categories": load_data().get("categories", [])}


@app.get("/api/tags")
async def get_tags():
    data = load_data()
    tags = sorted({tag for site in data.get("sites", []) for tag in site.get("tags", [])})
    return {"tags": tags}


@app.get("/api/stats")
async def get_stats():
    data = load_data()
    sites = data.get("sites", [])
    labels = category_lookup(data.get("categories", []))
    sections: dict[str, int] = {}
    for site in sites:
        key = site.get("primarySection") or "uncategorized"
        sections[key] = sections.get(key, 0) + 1
    return {
        "total": len(sites),
        "sections": [
            {"id": key, "name": labels.get(key, key), "count": count}
            for key, count in sorted(sections.items(), key=lambda item: -item[1])
        ],
        "tags": len({tag for site in sites for tag in site.get("tags", [])}),
        "capabilities": len({cap for site in sites for cap in site.get("capabilities", [])}),
    }


@app.get("/api/admin/overview")
async def get_admin_overview():
    data = load_data()
    stats = await get_stats()
    return {
        "stats": stats,
        "recentSites": data.get("sites", [])[:8],
        "dataFile": str(DATA_FILE),
    }
