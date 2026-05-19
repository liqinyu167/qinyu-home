# 好奇心导航 Demo

前后端分离演示项目。

## 技术栈

| 层 | 技术 | 说明 |
|----|------|------|
| 前端 | Astro 5 | 静态生成 + 客户端 JS 渲染 |
| 后端 | FastAPI | RESTful API，提供导航数据 |
| 网关 | Nginx | 反代，`/demo/` 静态，`/demo/api/` 转发后端 |

## 本地开发

### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

API 说明：

| 路由 | 说明 |
|------|------|
| `GET /api/health` | 健康检查 |
| `GET /api/sites` | 获取所有导航站 |
| `GET /api/stats` | 获取分类统计 |

### 前端

```bash
cd frontend
npm install
npm run dev
```

前端开发服务器默认 `http://localhost:4321`。前端 JS 中 `API_BASE` 默认指向 `/demo/api`，本地开发时需修改为后端地址（如 `http://localhost:8002/api`）。

### 构建部署

```bash
cd frontend
npm run build      # 输出到 frontend/dist/
```

构建产物由 Nginx 直接 serve 静态文件。

## 数据

`backend/sites.json` 是主站 `data/sites.json` 的独立副本。

## 架构示意

```
用户 → Nginx (443)
       ├── /demo/      → 静态文件 (frontend/dist/)
       └── /demo/api/*  → FastAPI (:8002)
                              └── sites.json
```
