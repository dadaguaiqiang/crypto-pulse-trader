import asyncio
import logging
from app.services.websocket.binance_client import binance_client
from app.services.data_processor.ticker_processor import ticker_processor

logger = logging.getLogger(__name__)


class WebSocketManager:
    def __init__(self):
        self.is_running = False
        self.task = None

    async def start(self):
        """启动 WebSocket 服务"""
        if self.is_running:
            logger.warning("WebSocket manager is already running")
            return

        self.is_running = True

        # 连接到 Binance
        success = await binance_client.connect()
        if not success:
            logger.error("Failed to start WebSocket manager: Connection failed")
            self.is_running = False
            return

        # 订阅交易对
        symbols = ["btcusdt", "ethusdt", "bnbusdt", "adausdt", "dotusdt",
                   "xrpusdt", "ltcusdt", "linkusdt", "bchusdt", "solusdt"]
        await binance_client.subscribe_ticker(symbols)

        # 启动消息监听
        self.task = asyncio.create_task(self._run_listener())
        logger.info("WebSocket manager started successfully")

    async def _run_listener(self):
        """运行消息监听器"""
        await binance_client.listen(ticker_processor.process_ticker_data)

    async def stop(self):
        """停止 WebSocket 服务"""
        self.is_running = False
        if self.task:
            self.task.cancel()
        await binance_client.disconnect()
        logger.info("WebSocket manager stopped")


# 全局实例
websocket_manager = WebSocketManager()