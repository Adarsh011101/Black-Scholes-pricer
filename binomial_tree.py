import numpy as np
from scipy.stats import norm

def binomial_tree(S,K,T,r,sigma,N,option_type='call'):
    """
    S : Stock Price
    K : Strike Price
    T : Time
    r : interest rate
    sigma : Volatility
    N : number of steps in binomial tree
    """

    dt = T/N  #lenght of each step
    u = np.exp(sigma*np.sqrt(dt))
    d = np.exp(-sigma*np.sqrt(dt))
    stock_prices = np.array([S*(u**j)*(d**(N-j)) for j in range(N+1)]) #stock prices at last nodes
    payoffs = np.maximum(stock_prices-K , 0) #Option payoffs

    p_tilda = (np.exp(r*dt) - d)/(u-d)
    q_tilda = 1 - p_tilda

    for _ in range(N):
        payoffs = np.exp(-r*dt)*(p_tilda*payoffs[1:] + q_tilda*payoffs[:-1])
    return payoffs[0]


def black_scholes(S,K,T,r,sigma,option_type='call'):
    
    """
    S : current stock price
    K : Strike Price
    r : risk free interest rate
    T : Time to maturity
    sigma : Volatility
    option type : call or put
    """
    d1 = (np.log(S/K)  + (r + 0.5*sigma**2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)

    if option_type == 'call':
        price = S*norm.cdf(d1) - K*(np.exp(-r*T))*norm.cdf(d2)
    else:
        price = K*(np.exp(-r*T))*norm.cdf(-d2) - S*norm.cdf(-d1)
    return price

    
import matplotlib.pyplot as plt
S= 150
K= 155
T = 30/365
r =0.05
sigma = 0.25

N_values = [10, 50, 100, 500, 1000]
prices = [binomial_tree(S, K, T, r, sigma, N) for N in N_values]
bs_price = black_scholes(S, K, T, r, sigma)

plt.figure(figsize=(10, 6))
plt.plot(N_values, prices, 'b-o', label='Binomial Tree')
plt.axhline(y=bs_price, color='red', linestyle='--', label=f'BS Price ${bs_price:.4f}')
plt.xlabel('Number of Steps (N)')
plt.ylabel('Option Price')
plt.title('Binomial Tree Convergence to Black-Scholes')
plt.legend()
plt.grid(True)
plt.show()






