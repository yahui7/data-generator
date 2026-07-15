"""
金融数据生成器 — 后端主应用
FastAPI + SQLite · 端口 8001
"""
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.data_generator.router import router as generator_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("[OK] 数据生成器启动完成 · 端口 8001")
    yield


app = FastAPI(
    title="金融数据生成器",
    description="一键生成模拟金融机构完整数据，可配置质量问题类型和比例",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generator_router, prefix="/api/generator", tags=["数据生成器"])

# 兼容旧版生成器前端：提供质量规则查询（返回空列表）
from fastapi import APIRouter as _APIRouter
_compat = _APIRouter()
@_compat.get("/rules")
async def get_rules():
    return {"status": "ok", "total": 0, "rules": []}
app.include_router(_compat, prefix="/api/quality", tags=["兼容"])


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "数据生成器运行中 · 端口 8001"}


# 前端静态文件
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
