# 白刀的 AIGC 工具箱

前后端分离版本已经从 `demo/` 迁移到正式应用目录。

## 目录

```text
apps/
  api/      FastAPI 数据接口
  web/      Astro 前台站点
  admin/    Astro 管理后台界面
data/
  sites.json
assets/
  favicons/
```

## 本地开发

### 后端

```bash
cd apps/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

### 前台

```bash
cd apps/web
npm install
npm run dev
```

默认地址：`http://127.0.0.1:4321/`

### 管理后台

```bash
cd apps/admin
npm install
npm run dev
```

默认地址：`http://127.0.0.1:4322/`

## API

| 路由 | 说明 |
| ---- | ---- |
| `GET /api/health` | 健康检查 |
| `GET /api/sites` | 工具列表，支持 `q`、`section`、`tag` |
| `GET /api/categories` | 分类 |
| `GET /api/tags` | 标签 |
| `GET /api/stats` | 统计 |
| `GET /api/admin/overview` | 后台概览数据 |

当前 API 读取根目录 `data/sites.json`。管理后台已搭好界面骨架，保存接口下一阶段接入。
