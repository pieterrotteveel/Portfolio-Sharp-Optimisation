# Simple Portfolio Optimizer

This script uses Python to build the "ideal" investment portfolio from a list of stocks. It automatically calculates how much of each stock you should buy to get the best possible return for the lowest possible risk.

### The Math Explained (Simply)

This script relies on **Modern Portfolio Theory**. It doesn't just pick the stocks that went up the most; it looks for the best *team* of stocks. Here are the three core concepts it uses:



#### 1. Volatility (Risk)
Think of volatility as the "bounciness" of a stock price.
* **Low Volatility:** The price moves slowly and steadily (like a calm ocean).
* **High Volatility:** The price swings wildly up and down (like a storm).
* **In the code:** We measure this using standard deviation ($\sigma$). The script tries to find a combination of stocks where the "bounciness" cancels out, making your ride smoother.

#### 2. Correlation (Diversification)
Correlation measures how two stocks move in relation to each other.
* **Positive Correlation (+1):** They move together (e.g., Google and Amazon often move up/down together).
* **Negative Correlation (-1):** They move in opposites (when one goes up, the other goes down).
* **Zero Correlation (0):** They ignore each other completely.
* **In the code:** The script calculates a **Covariance Matrix**. It prefers combining assets that *don't* move perfectly together. If one stock crashes, another might stay flat or go up, protecting your money.

#### 3. The Sharpe Ratio (The Goal)
This is the single number the script tries to maximize. It answers the question: **"Is the reward worth the risk?"**

The formula is:
$$\text{Sharpe Ratio} = \frac{R_p - R_f}{\sigma_p}$$

* $R_p$: The return of the portfolio.
* $R_f$: The "Risk-Free Rate" (what you'd get just putting cash in a safe bond, set to **4%** in this script).
* $\sigma_p$: The volatility (risk) of the portfolio.

**Translation:** If a portfolio has a high return but insane risk, it gets a *low* Sharpe Score. If it has moderate return but extremely low risk, it gets a *high* Sharpe Score. The script hunts for the mathematical maximum score.

---

### Prerequisites

You need Python installed along with these libraries:

```bash
pip install yfinance pandas numpy scipy