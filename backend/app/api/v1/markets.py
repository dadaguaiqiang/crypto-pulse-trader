from fastapi import APIRouter

router = APIRouter()

@router.get("/tickers")
async def get_tickers():
    # 临时模拟数据 - 在后续Sprint中替换为真实数据
    return {
        "BTCUSDT": {
            "symbol": "BTCUSDT",
            "price": 45000.50,
            "change_24h": 2.5,
            "volume_24h": 2500000000
        },
        "ETHUSDT": {
            "symbol": "ETHUSDT",
            "price": 2500.75,
            "change_24h": 1.2,
            "volume_24h": 1200000000
        }
    }