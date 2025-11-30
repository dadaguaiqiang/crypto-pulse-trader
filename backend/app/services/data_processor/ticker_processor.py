import logging
import redis
import json
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)


class TickerProcessor:
    def __init__(self):
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL)
        self.symbol_mapping = {
            "btcusdt": "BTCUSDT",
            "ethusdt": "ETHUSDT",
            "bnbusdt": "BNBUSDT",
            "adausdt": "ADAUSDT",
            "dotusdt": "DOTUSDT",
            "xrpusdt": "XRPUSDT",
            "ltcusdt": "LTCUSDT",
            "linkusdt": "LINKUSDT",
            "bchusdt": "BCHUSDT",
            "solusdt": "SOLUSDT"
        }

    async def process_ticker_data(self, data: Dict[str, Any]):
        """处理 ticker 数据"""
        try:
            # 检查是否是 ticker 数据
            if 'e' in data and data['e'] == '24hrTicker':
                symbol = data['s']  # 例如: BTCUSDT

                # 处理数据格式
                processed_data = {
                    'symbol': symbol,
                    'price': float(data['c']),  # 最新价格
                    'price_change': float(data['p']),  # 价格变化
                    'price_change_percent': float(data['P']),  # 价格变化百分比
                    'high_price': float(data['h']),  # 24小时最高价
                    'low_price': float(data['l']),  # 24小时最低价
                    'volume': float(data['v']),  # 基础资产交易量
                    'quote_volume': float(data['q']),  # 报价资产交易量
                    'last_update_id': data['u']  # 最后更新ID
                }

                # 存储到 Redis
                await self.store_to_redis(symbol, processed_data)
                logger.debug(f"Processed ticker data for {symbol}: {processed_data['price']}")

        except Exception as e:
            logger.error(f"Error processing ticker data: {e}")

    async def store_to_redis(self, symbol: str, data: Dict[str, Any]):
        """存储数据到 Redis"""
        try:
            # 存储单个交易对数据
            self.redis_client.hset(
                f"ticker:{symbol}",
                mapping=data
            )

            # 更新交易对列表
            self.redis_client.sadd("available_symbols", symbol)

            # 设置过期时间（1小时，防止数据陈旧）
            self.redis_client.expire(f"ticker:{symbol}", 3600)

        except Exception as e:
            logger.error(f"Error storing data to Redis: {e}")

    async def get_all_tickers(self) -> Dict[str, Dict[str, Any]]:
        """从 Redis 获取所有 ticker 数据"""
        try:
            symbols = self.redis_client.smembers("available_symbols")
            tickers = {}

            for symbol_bytes in symbols:
                symbol = symbol_bytes.decode('utf-8')
                ticker_data = self.redis_client.hgetall(f"ticker:{symbol}")

                if ticker_data:
                    # 转换字节数据为字符串和浮点数
                    processed_ticker = {}
                    for key, value in ticker_data.items():
                        key_str = key.decode('utf-8')
                        value_str = value.decode('utf-8')

                        # 尝试转换为浮点数，如果失败则保持字符串
                        try:
                            processed_ticker[key_str] = float(value_str)
                        except ValueError:
                            processed_ticker[key_str] = value_str

                    tickers[symbol] = processed_ticker

            return tickers

        except Exception as e:
            logger.error(f"Error getting tickers from Redis: {e}")
            return {}


# 全局实例
ticker_processor = TickerProcessor()