"""
Demo 后端 - FastAPI
白刀的好奇心网站 · 前后端分离演示
"""

import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="好奇心 API")

# 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = Path(__file__).parent / "sites.json"


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "好奇心 API 运行中"}


@app.get("/api/sites")
async def get_sites():
    """返回所有导航站数据"""
    if not DATA_FILE.exists():
        return {"sites": []}
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return data


@app.get("/api/stats")
async def get_stats():
    """返回导航站统计数据"""
    if not DATA_FILE.exists():
        return {"count": 0, "categories": []}
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    sites = data.get("sites", [])
    categories = {}
    for s in sites:
        cat = s.get("category", "未分类")
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "total": len(sites),
        "categories": [
            {"name": k, "count": v}
            for k, v in sorted(categories.items(), key=lambda x: -x[1])
        ],
    }
