import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Task 1

tickers = ['AAPL', 'VEA', 'BND', 'GLD', 'VNQ', 'USO', 'BTC-USD', 'VWO', 'IWM', 'TIP']
start_date = '2014-01-01'
end_date = '2024-12-31'

data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
adj_close = data['Adj Close']
close = data['Close']


# Task 2

#def drop_large_nan_streaks(df, threshold=5):
    #is_na = df.isna()
    #streaks = is_na.astype(int).groupby(is_na.cumsum()).cumsum()
    #return df[(streaks <= threshold) | ~is_na].ffill()

adj_close = adj_close.interpolate(method='linear', limit=5)
adj_close_cleaned = adj_close.ffill()


# Task 3

weights = {
    'AAPL': 0.10, 'VEA': 0.10, 'BND': 0.15, 'GLD': 0.10, 'VNQ': 0.10,
    'USO': 0.05, 'BTC-USD': 0.10, 'VWO': 0.10, 'IWM': 0.10, 'TIP': 0.10
}
weights_series = pd.Series(weights)
daily_returns = adj_close_cleaned.pct_change().dropna()
weighted_returns = daily_returns.mul(weights_series, axis=1)
portfolio_returns = weighted_returns.sum(axis=1)
portfolio_df = pd.DataFrame({
    'Portfolio Return': portfolio_returns,
    'Cumulative Return': (1 + portfolio_returns).cumprod()
})


# Task 4

risk_free_rate = 0.045
cumulative_return = portfolio_df['Cumulative Return'].iloc[-1] - 1
annualized_return = (1 + cumulative_return) ** (1/10) - 1
annualized_volatility = portfolio_df['Portfolio Return'].std() * np.sqrt(252)
sharpe_ratio = (annualized_return - risk_free_rate) / annualized_volatility
cumulative = (1 + portfolio_returns).cumprod()
rolling_max = cumulative.cummax()
drawdown = (cumulative - rolling_max) / rolling_max
max_drawdown = drawdown.min()
drawdown_duration = (drawdown < 0).astype(int).groupby(drawdown.ne(0).cumsum()).cumsum().max()

print("\n=== Performance Metrics ===")
print(f"Cumulative Return:     {cumulative_return:.2%}")
print(f"Annualized Return:     {annualized_return:.2%}")
print(f"Annualized Volatility: {annualized_volatility:.2%}")
print(f"Sharpe Ratio:          {sharpe_ratio:.2f}")
print(f"Max Drawdown:          {max_drawdown:.2%}")
print(f"Drawdown Duration:     {drawdown_duration} days")


# Task 5

correlation_matrix = daily_returns.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
plt.title("Asset Correlation Matrix")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

rolling_corr_btc_spy = daily_returns['BTC-USD'].rolling(90).corr(daily_returns['AAPL'])
rolling_corr_gold_bond = daily_returns['GLD'].rolling(90).corr(daily_returns['BND'])

plt.figure(figsize=(12, 6))
plt.plot(rolling_corr_btc_spy, label='BTC-USD vs AAPL')
plt.plot(rolling_corr_gold_bond, label='GLD vs BND')
plt.title("Rolling 90-Day Correlation")
plt.ylabel("Correlation")
plt.xlabel("Date")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Task 6

# Cumulative return
plt.figure(figsize=(10, 5))
plt.plot(portfolio_df['Cumulative Return'], label='Portfolio')
plt.title("Cumulative Return Over Time")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Rolling volatility
rolling_vol = daily_returns.rolling(252).std() * np.sqrt(252)
portfolio_rolling_vol = portfolio_returns.rolling(252).std() * np.sqrt(252)

plt.figure(figsize=(12, 6))
plt.plot(portfolio_rolling_vol, label='Portfolio', linewidth=2)
plt.plot(rolling_vol[['AAPL', 'GLD', 'BTC-USD', 'BND']], linestyle='--')
plt.title('Rolling 1-Year Volatility')
plt.ylabel('Volatility')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Drawdown
plt.figure(figsize=(10, 5))
plt.fill_between(drawdown.index, drawdown, color='red', alpha=0.4)
plt.title('Portfolio Drawdown Curve')
plt.xlabel('Date')
plt.ylabel('Drawdown (%)')
plt.grid(True)
plt.tight_layout()
plt.show()


# Task 7

mean_returns = daily_returns.mean() * 252
cov_matrix = daily_returns.cov() * 252

num_portfolios = 5000
results = np.zeros((3, num_portfolios))
weights_record = []

np.random.seed(42)
for i in range(num_portfolios):
    w = np.random.random(len(tickers))
    w /= np.sum(w)
    weights_record.append(w)

    port_return = np.dot(w, mean_returns)
    port_vol = np.sqrt(np.dot(w.T, np.dot(cov_matrix, w)))
    sharpe = (port_return - risk_free_rate) / port_vol

    results[0, i] = port_return
    results[1, i] = port_vol
    results[2, i] = sharpe

results_df = pd.DataFrame(results.T, columns=['Return', 'Volatility', 'Sharpe'])
weights_df = pd.DataFrame(weights_record, columns=tickers)

max_sharpe_idx = results_df['Sharpe'].idxmax()
min_vol_idx = results_df['Volatility'].idxmin()

print("\n=== Maximum Sharpe Portfolio ===")
print(weights_df.iloc[max_sharpe_idx].round(4))
print(results_df.loc[max_sharpe_idx])

print("\n=== Minimum Volatility Portfolio ===")
print(weights_df.iloc[min_vol_idx].round(4))
print(results_df.loc[min_vol_idx])

# Efficient Frontier plot
plt.figure(figsize=(10, 6))
plt.scatter(results_df['Volatility'], results_df['Return'], c=results_df['Sharpe'], cmap='viridis', s=10, alpha=0.5)
plt.scatter(results_df.loc[max_sharpe_idx, 'Volatility'], results_df.loc[max_sharpe_idx, 'Return'], c='red', marker='*', s=100, label='Max Sharpe')
plt.scatter(results_df.loc[min_vol_idx, 'Volatility'], results_df.loc[min_vol_idx, 'Return'], c='blue', marker='*', s=100, label='Min Volatility')
plt.colorbar(label='Sharpe Ratio')
plt.title('Efficient Frontier')
plt.xlabel('Volatility (Risk)')
plt.ylabel('Expected Return')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()