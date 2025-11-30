import asyncio
import json
import logging
from typing import Dict, Callable, Any
import aiohttp
import websockets
from app.core.config import settings

logger = logging.getLogger(__name__)


class BinanceWebSocketClient:
    def __init__(self):
        self.base_url = "wss://stream.binance.com:9443/ws"
        self.websocket = None
        self.is_connected = False
        self.subscriptions = set()
        self.message_handlers = []

    async def connect(self):
        """连接到 Binance WebSocket"""
        try:
            self.websocket = await websockets.connect(self.base_url)
            self.is_connected = True
            logger.info("Connected to Binance WebSocket")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Binance WebSocket: {e}")
            return False

    async def subscribe_ticker(self, symbols: list):
        """订阅指定交易对的 ticker 数据"""
        if not self.is_connected:
            await self.connect()

        streams = [f"{symbol.lower()}@ticker" for symbol in symbols]
        subscription_msg = {
            "method": "SUBSCRIBE",
            "params": streams,
            "id": 1
        }

        await self.websocket.send(json.dumps(subscription_msg))
        self.subscriptions.update(streams)
        logger.info(f"Subscribed to ticker streams: {streams}")

    async def listen(self, message_handler: Callable):
        """监听 WebSocket 消息"""
        self.message_handlers.append(message_handler)

        while self.is_connected:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)

                # 调用所有注册的消息处理器
                for handler in self.message_handlers:
                    await handler(data)

            except websockets.exceptions.ConnectionClosed:
                logger.error("WebSocket connection closed")
                self.is_connected = False
                break
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}")
                continue

    async def disconnect(self):
        """断开连接"""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            logger.info("Disconnected from Binance WebSocket")


# 全局实例
binance_client = BinanceWebSocketClient()