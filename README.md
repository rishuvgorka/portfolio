# 📊 Multi-Asset Portfolio Analysis

This project performs a comprehensive financial analysis of a diversified, multi-asset investment portfolio using Python. It calculates key performance metrics, visualizes correlations and volatilities, simulates thousands of portfolios, and plots the efficient frontier.

---

## 📁 Features

- ✅ Historical price data collection using `yfinance`
- ✅ Portfolio return calculation with custom weights
- ✅ Performance metrics: Cumulative Return, Annualized Return, Volatility, Sharpe Ratio, Max Drawdown
- ✅ Asset correlation analysis and rolling correlations
- ✅ Visualizations: cumulative return, volatility trends, drawdowns
- ✅ Monte Carlo simulation of 5000 random portfolios
- ✅ Efficient frontier and optimal portfolio identification

---

## 🧾 Portfolio Assets

The portfolio consists of the following 10 assets:

| Asset Type        | Ticker     |
|-------------------|------------|
| US Equities       | AAPL, IWM  |
| International Eq. | VEA, VWO   |
| Bonds             | BND, TIP   |
| Commodities       | GLD, USO   |
| Real Estate       | VNQ        |
| Cryptocurrency    | BTC-USD    |

---

## 🧮 Libraries Used

- `yfinance`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`

Install them via:

```bash
pip install yfinance pandas numpy matplotlib seaborn
```

---

## 🚀 How to Run

1. Clone the repository or download the script.
2. Install dependencies (see above).
3. Run the script using Python:

```bash
python "multiasset portfolio analysis.py"
```

---

## 📊 Key Analysis Sections

### 1. Data Collection
Fetches adjusted and raw close prices from Yahoo Finance from 2014 to 2024.

### 2. Data Cleaning
Interpolates missing values and applies forward fill to clean the dataset.

### 3. Portfolio Construction
Applies predefined weights to calculate daily and cumulative portfolio returns.

### 4. Performance Metrics
Calculates:
- **Cumulative Return**
- **Annualized Return**
- **Annualized Volatility**
- **Sharpe Ratio** (assumed risk-free rate: 4.5%)
- **Maximum Drawdown** and its duration

### 5. Correlation Analysis
- Correlation heatmap between all assets
- 90-day rolling correlations:
  - BTC-USD vs AAPL
  - GLD vs BND

### 6. Visualizations
- Cumulative return chart
- Rolling volatility plots
- Drawdown curve
- Correlation matrix

### 7. Portfolio Optimization
- Simulates 5000 random portfolios
- Calculates return, volatility, Sharpe ratio
- Identifies optimal and minimum-risk portfolios
- Plots the **Efficient Frontier**

---

## 📌 Notes

- Portfolio weights can be customized in the `weights` dictionary.
- The analysis uses a fixed 10-year period (2014–2024) which you can adjust.
- Monte Carlo simulation helps visualize risk-return tradeoffs.

---

## 📄 License

This project is licensed under the MIT License. Feel free to fork, modify, and use it for educational or commercial purposes.

---

## ✍️ Author

Made with ❤️ by [Your Name]