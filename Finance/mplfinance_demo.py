import mplfinance as mpf
import yfinance as yf

nvidia = yf.Ticker("NVDA")
df = nvidia.history(start="2025-10-01", end="2025-12-31")
print(df.info())

mpf.plot(df, type='ohlc', title="OHLC")
mpf.plot(df, type='candle', title="Candle")
mpf.plot(df, type='line', title="Line")
mpf.plot(df, type='renko', title="Renko")
mpf.plot(df, type='pnf', title="PNF")
mpf.plot(df, type='candle',volume=True, title="Candle With Volume")
mpf.plot(df, type='candle',mav=(7,12), title="Candle + Moving Average 7 & 12 Days")
mpf.plot(df, type='candle',mav=(5,10,20), title="Candle + Moving Average 5, 10 & 20 Days")