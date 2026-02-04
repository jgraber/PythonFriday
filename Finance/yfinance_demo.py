import yfinance as yf
import pprint

nvidia = yf.Ticker("NVDA")

df = nvidia.history("5d")
print(df.info())
print(df)

print("*" * 50)

pprint.pp(nvidia.info["shortName"])
pprint.pp(nvidia.info)

print("*" * 50)

pprint.pp(nvidia.calendar)


print("*" * 50)

start = "2024-01-01"
end = "2025-12-31"
stocks = ["AAPL", "GOOG", "MSFT","NVDA"]

historic_prices = yf.Tickers(stocks).history(start=start, end=end)
print(historic_prices.info())
print(historic_prices)