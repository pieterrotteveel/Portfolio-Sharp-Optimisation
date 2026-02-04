import yfinance as yf
import pandas as pd
import numpy as np
from scipy.optimize import minimize

# User Configuration

tickers = [
    'GOOG', 'AMZN', 'IBM', 'AMAT', 'SMSD.L', 'AAPL',
    'BAC', 'HSBC', 'INGA.AS', 'STT', 'CS.PA', '3988.HK',
    'SHEL.L', '0857.HK', 'GOLD', '0358.HK', 'LMT', 'RTX', 'HEI.DE', 'PLD', 'NEE',
    'KO', 'PEP', 'COST', 'MCD', 'ULVR.L', 'PM', 'UNH', 'ABBV', 'DMP.DE', 'T'
]

start_date = '2000-01-01'
end_date = '2024-01-01'
risk_free_rate = 0.04 


ALLOW_SHORT_SELLING = False   
MAX_WEIGHT = 0.15            
MIN_WEIGHT = -0.05      


# Data Processing

raw_data = yf.download(tickers, start=start_date, end=end_date)['Close']

# Clean data: Remove empty columns and fill gaps
raw_data = raw_data.dropna(axis=1, how='all')
data = raw_data.ffill().dropna()

print(f"Final Data Shape: {data.shape}")

# Calculate stats
returns = data.pct_change().dropna()
mean_returns = returns.mean() * 252
cov_matrix = returns.cov() * 252

# Optimization Logic

def negative_sharpe(weights, mean_returns, cov_matrix, risk_free_rate):
    p_return = np.sum(returns.mean() * weights) * 252
    p_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    if p_std == 0: return 0
    sharpe = (p_return - risk_free_rate) / p_std
    return -sharpe 

valid_tickers = data.columns.tolist()
num_assets = len(valid_tickers)


if ALLOW_SHORT_SELLING:
    lower_bound = MIN_WEIGHT
    upper_bound = MAX_WEIGHT
else:
    lower_bound = 0.0
    upper_bound = MAX_WEIGHT

bounds = tuple((lower_bound, upper_bound) for _ in range(num_assets))
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
init_guess = [1/num_assets] * num_assets

result = minimize(
    negative_sharpe, 
    init_guess, 
    args=(mean_returns, cov_matrix, risk_free_rate),
    method='SLSQP', 
    bounds=bounds, 
    constraints=constraints
)

# Results Display

optimal_weights = result.x
portfolio = pd.DataFrame({'Ticker': valid_tickers, 'Weight': optimal_weights})

portfolio['Action'] = np.where(portfolio['Weight'] > 0.001, 'BUY', 
                               np.where(portfolio['Weight'] < -0.001, 'SHORT', '-'))

active_portfolio = portfolio[portfolio['Weight'].abs() > 0.001].sort_values(by='Weight', ascending=False)

print("\n--- Optimized Portfolio Allocation ---")
print(active_portfolio[['Ticker', 'Action', 'Weight']].round(4))

print(f"\nMax Sharpe Ratio: {-result.fun:.4f}")

long_exposure = active_portfolio[active_portfolio['Weight'] > 0]['Weight'].sum()
short_exposure = active_portfolio[active_portfolio['Weight'] < 0]['Weight'].sum()

print(f"\nTotal Long Exposure:  {long_exposure:.2%}")
print(f"Total Short Exposure: {short_exposure:.2%}")
print(f"Net Investment:       {long_exposure + short_exposure:.2%}")