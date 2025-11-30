from fastapi import APIRouter, HTTPException
from app.services.data_processor.ticker_processor import ticker_processor

router = APIRouter()


@router.get("/tickers")
async def get_tickers():
    """获取所有交易对的实时价格数据"""
    try:
        tickers = await ticker_processor.get_all_tickers()

        # 如果没有数据，返回模拟数据（开发期间）
        if not tickers:
            return get_mock_tickers()

        return tickers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch tickers: {str(e)}")


@router.get("/tickers/{symbol}")
async def get_ticker(symbol: str):
    """获取指定交易对的实时价格数据"""
    try:
        tickers = await ticker_processor.get_all_tickers()
        symbol_upper = symbol.upper()

        if symbol_upper in tickers:
            return tickers[symbol_upper]
        else:
            raise HTTPException(status_code=404, detail=f"Ticker {symbol} not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch ticker: {str(e)}")


def get_mock_tickers():
    """模拟数据（当真实数据不可用时）"""
    return {
        "BTCUSDT": {
            "symbol": "BTCUSDT",
            "price": 45000.50,
            "price_change": 500.25,
            "price_change_percent": 1.12,
            "high_price": 45500.75,
            "low_price": 44800.25,
            "volume": 12500.5,
            "quote_volume": 562522500.0,
            "last_update_id": "mock_001"
        },
        "ETHUSDT": {
            "symbol": "ETHUSDT",
            "price": 2500.75,
            "price_change": 25.50,
            "price_change_percent": 1.03,
            "high_price": 2520.25,
            "low_price": 2480.50,
            "volume": 85000.25,
            "quote_volume": 212563750.0,
            "last_update_id": "mock_002"
        }
    }