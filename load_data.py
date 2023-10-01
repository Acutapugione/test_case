import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime


symbol = "BTCUSDT"
interval = "1m"
start_date = "2019-09-30T00:00:00"
end_date = "2024-09-30T02:00:00"
client = Client()
klines = client.get_historical_klines(symbol, interval, start_date, end_date,)
df = pd.DataFrame(klines, columns=[
    "OpenTime", "Open", "High", "Low", "Close", "Volume", "CloseTime", "QuoteVolume", "NumberOfTrades", "TakerBuyBaseVolume", "TakerBuyQuoteVolume", "Ignore",
])
df.to_csv(f'{symbol}_{interval}_{datetime.now().strftime("%d_%m_%y")}.csv')