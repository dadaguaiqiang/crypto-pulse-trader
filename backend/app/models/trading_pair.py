from sqlalchemy import Column, String, Boolean
from app.models.base import  aseModel


class TradingPair(BaseModel):
    __tablename__ = "trading_pairs"

    symbol = Column(String(20), unique=True, index=True, nullable=False)
    base_asset = Column(String(10), nullable=False)
    quote_asset = Column(String(10), nullable=False)
    is_active = Column(Boolean, default=True)