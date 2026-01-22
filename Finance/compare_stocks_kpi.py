import yfinance as yf
import pandas as pd
import math

# --------------------------------------------------
# Configuration
# --------------------------------------------------
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL"]

kpis = {
    "Market Cap": ("marketCap", "currency"),
    "Forward P/E": ("forwardPE", "ratio"),
    "PEG Ratio": ("pegRatio", "ratio"),
    "Price-to-Sales": ("priceToSalesTrailing12Months", "ratio"),
    "Revenue Growth (YoY)": ("revenueGrowth", "percent"),
    "EPS Growth (YoY)": ("earningsGrowth", "percent"),
    "Gross Margin": ("grossMargins", "percent"),
    "Operating Margin": ("operatingMargins", "percent"),
    "Free Cash Flow": ("freeCashflow", "currency"),
    "Debt-to-Equity": ("debtToEquity", "ratio"),
    "Current Ratio": ("currentRatio", "ratio"),
    "Beta": ("beta", "ratio"),
}

# --------------------------------------------------
# Formatting helpers
# --------------------------------------------------
def format_currency(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    abs_value = abs(value)
    if abs_value >= 1e12:
        return f"${value / 1e12:.2f}T"
    if abs_value >= 1e9:
        return f"${value / 1e9:.2f}B"
    if abs_value >= 1e6:
        return f"${value / 1e6:.2f}M"
    return f"${value:,.0f}"

def format_percent(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    return f"{value * 100:.1f} %"

def format_ratio(value):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    return f"{value:.2f}"

# --------------------------------------------------
# Data collection
# --------------------------------------------------
data = {}

for ticker in tickers:
    t = yf.Ticker(ticker)
    info = t.info
    
    row = {}
    for kpi_name, (info_key, fmt) in kpis.items():
        raw = info.get(info_key)
        
        if fmt == "currency":
            row[kpi_name] = format_currency(raw)
        elif fmt == "percent":
            row[kpi_name] = format_percent(raw)
        else:
            row[kpi_name] = format_ratio(raw)
    
    data[ticker] = row

# --------------------------------------------------
# Build table
# --------------------------------------------------
df = pd.DataFrame(data)

print(df)
