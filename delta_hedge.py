import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from Black_scholes import black_scholes

#Computing Delta using BS
def BS(S,K,T,r,sigma):
    d1 = (np.log(S/K)+(r + 0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    delta = norm.cdf(d1)
    return delta

#Simulate Geometric Brownian Motion
def simulate_stock(S,T,r,sigma,N):
    dt = T/N
    prices = [S]
    for _ in range(N):
        Z = np.random.standard_normal()
        S_next = prices[-1] *np.exp((r - 0.5*sigma**2)*dt + sigma*np.sqrt(dt)*Z)
        prices.append(S_next)
    return np.array(prices)

def delta_hedging_function(S,K,T,r,sigma,N):
    prices = simulate_stock(S,T,r,sigma,N)

    deltas = []
    for i in range(N):
        T_remaining = (N-i)/365
        d = BS(prices[i],K,T_remaining,r,sigma)
        deltas.append(d)
    """for i in range(len(deltas)):
        print(f"Day {i}: S={prices[i]:.2f}, delta={deltas[i]:.4f}")
    """
    #Trading Option and share
    call_premimum = black_scholes(S,K,T,r,sigma,'call')
    cash = call_premimum - deltas[0]*S  # intial cash in hand 
    shares = deltas[0]

    pnl=[]

    for i in range(N):
        cash *= np.exp(r*(1/365)) # cash grows at risk free rate

        # Rebalance Share
        new_share = deltas[i]
        cash -= ( new_share - shares)*prices[i]  #buy/sell shares based on delta
        shares = new_share
    #last day/expiry
    cash *= np.exp(r*(1/365))
    option_payoff = max(prices[-1]-K,0)
    final_pnl = cash + shares*prices[-1] - option_payoff
    return final_pnl

if '__name__' == '__name__':
    pnls = [delta_hedging_function(150,155,30/365,0.05,0.25,30) for _ in range(1000)]
    print(f"Mean P&L: ${np.mean(pnls):.4f}")
    print(f"Std P&L: ${np.std(pnls):.4f}")
    #graphical view
    plt.hist(pnls, bins=50, edgecolor='black')
    plt.axvline(x=0, color='red', linestyle='--', label='Zero P&L')
    plt.xlabel('P&L ($)')
    plt.ylabel('Frequency')
    plt.title('Delta Hedging P&L Distribution (1000 simulations)')
    plt.legend()
    plt.grid(True)
    plt.show()







