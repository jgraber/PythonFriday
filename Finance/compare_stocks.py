import yfinance as yf
import matplotlib.pyplot as plt

def plot_closing_prices(data):
    close_prices = data["Close"]
    price_change_in_percentage = (close_prices / close_prices.iloc[0] * 100)
    print(price_change_in_percentage)
    price_change_in_percentage.plot(figsize = (12,8), fontsize = 12)
    plt.ylabel("Percentage")
    plt.title(f"Price Chart", fontsize = 15)
    plt.show()
    
    
start = "2024-01-01"
end = "2025-12-31"
stocks = ["NVDA", "MSFT","GOOG"]

historic_prices = yf.Tickers(stocks).history(start=start, end=end)
# print(historic_prices)
plot_closing_prices(historic_prices)