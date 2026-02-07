import yfinance as yf
import pandas as pd


def load_price_data(ticker, start, end=None):
    df = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df[['Close']].copy()
# --------------------------------------------------------
from abc import ABC, abstractmethod


class TradingStrategy(ABC):
    @abstractmethod
    def prepare_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add indicators needed by the strategy"""
        pass

    @abstractmethod
    def generate_signal(self, df: pd.DataFrame, i: int, position: int) -> str | None:
        """
        Return:
        - "BUY"
        - "SELL"
        - None
        """
        pass

# --------------------------------------------------------
class BollingerBandsStrategy(TradingStrategy):
    def __init__(self, window=20, num_std=2):
        self.window = window
        self.num_std = num_std

    def prepare_indicators(self, df):
        df = df.copy()
        df['SMA'] = df['Close'].rolling(self.window).mean()
        df['STD'] = df['Close'].rolling(self.window).std()
        df['Upper'] = df['SMA'] + self.num_std * df['STD']
        df['Lower'] = df['SMA'] - self.num_std * df['STD']
        return df

    def generate_signal(self, df, i, position):
        price = df['Close'].iloc[i]
        prev_price = df['Close'].iloc[i - 1]

        lower = df['Lower'].iloc[i]
        prev_lower = df['Lower'].iloc[i - 1]

        upper = df['Upper'].iloc[i]
        prev_upper = df['Upper'].iloc[i - 1]

        if (
            position == 0
            and prev_price > prev_lower
            and price < lower
        ):
            return "BUY"

        if (
            position > 0
            and prev_price < prev_upper
            and price > upper
        ):
            return "SELL"

        return None
    

class MovingAverageCrossoverStrategy(TradingStrategy):
    def __init__(
        self,
        fast_window=50,
        slow_window=200,
        ma_type="SMA"  # "SMA" or "EMA"
    ):
        self.fast_window = fast_window
        self.slow_window = slow_window
        self.ma_type = ma_type.upper()

    def prepare_indicators(self, df):
        df = df.copy()

        if self.ma_type == "EMA":
            df['MA_fast'] = df['Close'].ewm(
                span=self.fast_window,
                adjust=False
            ).mean()
            df['MA_slow'] = df['Close'].ewm(
                span=self.slow_window,
                adjust=False
            ).mean()
        else:  # SMA default
            df['MA_fast'] = df['Close'].rolling(
                self.fast_window
            ).mean()
            df['MA_slow'] = df['Close'].rolling(
                self.slow_window
            ).mean()

        return df

    def generate_signal(self, df, i, position):
        fast = df['MA_fast'].iloc[i]
        fast_prev = df['MA_fast'].iloc[i - 1]

        slow = df['MA_slow'].iloc[i]
        slow_prev = df['MA_slow'].iloc[i - 1]

        # BUY: fast MA crosses above slow MA
        if (
            position == 0
            and fast_prev < slow_prev
            and fast > slow
        ):
            return "BUY"

        # SELL: fast MA crosses below slow MA
        if (
            position > 0
            and fast_prev > slow_prev
            and fast < slow
        ):
            return "SELL"

        return None

# --------------------------------------------------------
class StrategyTester:
    def __init__(self, initial_cash=10_000):
        self.initial_cash = initial_cash

    def run(self, df, strategy: TradingStrategy):
        df = strategy.prepare_indicators(df)

        cash = self.initial_cash
        shares = 0
        trades = []

        for i in range(1, len(df)):
            signal = strategy.generate_signal(df, i, shares)
            price = float(df['Close'].iloc[i])

            if signal == "BUY" and shares == 0:
                shares = cash / price
                cash = 0
                trades.append((df.index[i], price, "BUY"))

            elif signal == "SELL" and shares > 0:
                cash = shares * price
                shares = 0
                trades.append((df.index[i], price, "SELL"))

        final_value = cash + shares * df['Close'].iloc[-1]

        return {
            "final_value": final_value,
            "return_pct": (final_value / self.initial_cash - 1) * 100,
            "trades": trades,
            "df": df
        }
        
    def baseline(self, df):
        cash = self.initial_cash
        trades = []
        
        first = float(df['Close'].iloc[0])
        trades.append((df.index[0], first, "BUY"))
        
        last = float(df['Close'].iloc[-1])
        trades.append((df.index[-1], last, "SELL"))
        
        shares = cash / first
        final_value = shares * last
        
        return {
            "final_value": final_value,
            "return_pct": (final_value / self.initial_cash - 1) * 100,
            "trades": trades,
            "df": df
        }
        
    def print_result(self, result, label):
        print(f"========= {label} =========")
        print(f"Final value: ${result['final_value']:,.2f}")
        print(f"Return: {result['return_pct']:.2f}%")
        print(f"Trades:")
        for trade in result['trades']:
            print(trade)
        print(f"\n==================================\n\n")

# --------------------------------------------------------
import matplotlib.pyplot as plt


def plot_results(df, trades, title):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['Close'], label="Close", linewidth=1.2)

    for col in ['SMA', 'Upper', 'Lower']:
        if col in df.columns:
            plt.plot(df.index, df[col], linestyle="--", label=col)

    for date, price, action in trades:
        marker = "^" if action == "BUY" else "v"
        plt.scatter(date, price, marker=marker, s=100, zorder=5)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# --------------------------------------------------------

# Parameters
TICKER = "NVDA"
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

# Fetch data
df = load_price_data(TICKER, START_DATE, END_DATE)

# Initialise classes
# strategy = BollingerBandsStrategy(window=20, num_std=2)
strategy = MovingAverageCrossoverStrategy(12, 26, "SMA")
# strategy_name = "Bollinger Bands"
strategy_name = "Moving Average Crossover"
tester = StrategyTester(initial_cash=10_000)

# Benchmark
benchmark = tester.baseline(df)
tester.print_result(benchmark, "Benchmark: Buy & Hold")
   
# Test strategy
result = tester.run(df, strategy)
tester.print_result(result, strategy_name)
    
plot_results(
    result['df'],
    result['trades'],
    title=f"{TICKER} – {strategy_name} Strategy"
)

