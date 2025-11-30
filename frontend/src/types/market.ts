export interface TickerData {
  symbol: string;
  price: number;
  change_24h: number;
  volume_24h: number;
}

export interface MarketState {
  tickers: Record<string, TickerData>;
  loading: boolean;
  error: string | null;
}