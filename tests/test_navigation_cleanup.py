#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
source = root / "apps/web/src/pages/index.astro"
text = source.read_text(encoding="utf-8")

removed = {
    "笔记占位": ">笔记<",
    "模板占位": ">模板<",
    "素材占位": ">素材<",
    "恐龙游戏入口": "dinoGameButton",
    "恐龙游戏弹窗": "gameDialog",
    "无效投稿邮箱": "submit@example.com",
}
required = {
    "个人介绍": "personalIntroBtn",
    "模型大比拼": "modelsToggle",
    "网站列表": "websitesToggle",
    "收藏": "favoritesButton",
    "随机发现": "randomButton",
    "封面hidden规则": ".hero[hidden]",
}

errors = []
for name, marker in removed.items():
    if marker in text:
        errors.append(f"仍存在{name}: {marker}")
for name, marker in required.items():
    if marker not in text:
        errors.append(f"误删核心入口{name}: {marker}")

sitemap = (root / "sitemap.xml").read_text(encoding="utf-8")
if "games/dino.html" in sitemap:
    errors.append("sitemap仍包含已删除的恐龙游戏URL")
if (root / "games/dino.html").exists():
    errors.append("恐龙游戏资源文件仍存在")
if (root / "apps/web/public/games").exists() or (root / "apps/web/public/games").is_symlink():
    errors.append("public/games残留或成为悬空符号链接")

if errors:
    print("NAV_CLEANUP_FAIL")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("NAV_CLEANUP_OK")
