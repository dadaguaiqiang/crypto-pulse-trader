from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.init import api_router
from app.services.websocket.manager import websocket_manager
from app.core.logging import setup_logging

# 设置日志
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时
    print("Starting WebSocket manager...")
    await websocket_manager.start()

    yield

    # 关闭时
    print("Stopping WebSocket manager...")
    await websocket_manager.stop()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan  # 添加生命周期管理
)

# 设置 CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# 包含 API 路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": "Welcome to CryptoPulse Trader API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)