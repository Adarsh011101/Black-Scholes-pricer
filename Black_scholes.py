import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.stats import norm

#Deriving call and put price using the Black_Scholes model
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

#Calculating Greeks
def greeks(S,K,T,r,sigma,option_type = 'call'):
    d1 = (np.log(S/K)  + (r + 0.5*sigma**2) * T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    #Delta
    if option_type == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    
    #Gamma
    gamma = norm.pdf(d1)/(S*sigma*np.sqrt(T))

    #Theta - per day
    if option_type == 'call':
        Theta = (-S*norm.pdf(d1) *sigma/(2*np.sqrt(T)) - r*K*np.exp(-r*T)*norm.cdf(d2))/365
    else:
        Theta = (-S*norm.pdf(d1) *sigma/(2*np.sqrt(T)) + r*K*np.exp(-r*T)*norm.cdf(-d2))/365
    #vega
    vega = S*np.sqrt(T)*norm.pdf(d1)/100
    #rho- per 1% change in interest rate
    if option_type=='call':
        rho = K*T*np.exp(-r*T)*norm.cdf(d2) /100
    else:
        rho = -K*T*np.exp(-r*T)*norm.cdf(-d2) /100
    return {'delta': delta , 'gamma' : gamma,'theta' : Theta , 'vega' : vega,'rho' :rho}


# Calculating impied Volatilty using Bisection method

def implied_volatility(market_price,S,K,T,r,option_type ='call'):
    sigma_low = 0.001
    sigma_high = 5.0
    tolerance= 1e-6
    
    for _ in range(1000): #max_iteration
        sigma_mid = (sigma_low + sigma_high) *0.5
        price = black_scholes(S,K,T,r,sigma_mid,option_type)
        if abs(price - market_price) < tolerance :
            return sigma_mid
        elif price>market_price:
            sigma_high = sigma_mid
        else:
            sigma_low = sigma_mid
    return sigma_mid




if __name__=='__main__':
    # Example: AAPL-like parameters
    S = 150       # current stock price
    K = 155       # strike price
    T = 30/365    # 30 days to expiration
    r = 0.05      # 5% risk-free rate
    sigma = 0.25  # 25% volatility
    
    call_price = black_scholes(S, K, T, r, sigma, 'call')
    put_price = black_scholes(S, K, T, r, sigma, 'put')
 
    print(f"Call Price: ${call_price:.4f}")
    print(f"Put Price:  ${put_price:.4f}")
    print()
 
    # Verify put-call parity: C - P = S - K*e^(-rT)
    lhs = call_price - put_price
    rhs = S - K * np.exp(-r * T)
    print(f"Put-Call Parity Check: C-P = {lhs:.4f}, S-Ke^(-rT) = {rhs:.4f}")
    print()
 
    g = greeks(S, K, T, r, sigma, 'call')
    print("Call Greeks:")
    for name, val in g.items():
        print(f"  {name}: {val:.6f}")

    impiled_vol = implied_volatility(call_price,S,K,T,r,'call')
    print(f"Implied Volatility : {impiled_vol:.4f}")

    #Plotting Volatility Skew

    ticker = yf.Ticker("AAPL")
    spot = ticker.history(period='1d')['Close'].iloc[-1]
    #print(f"AAPL spot: ${spot:.2f}")

    chain = ticker.option_chain('2026-10-26')
    calls = chain.calls
    #print(calls[['strike', 'lastPrice', 'impliedVolatility']])
    calls = calls[calls['impliedVolatility']>0.01]
    atm = calls[(calls['strike'].between(280, 400)) & (calls['impliedVolatility'] < 2.0)]


    #calculating last 1 year volatility
    hist = ticker.history(period='1y')['Close']
    returns = hist.pct_change().dropna()
    hist_vol = returns.std()*np.sqrt(252)*100 #in percentage



    plt.figure(figsize=(10,6))
    plt.plot(atm['strike'] , atm['impliedVolatility']*100,'b-o',markersize =4)
    plt.axvline(x=spot, color='red', linestyle='--', label=f'Spot ${spot:.2f}')
    plt.axhline(y=hist_vol,color='green' , linestyle='--',label=f'Historical Vol {hist_vol:.2f}%')
    plt.xlabel('Strike Price')
    plt.ylabel('Implied Volatility (%)')
    plt.title('AAPL Volatility Skew - Oct 2026')
    plt.legend()
    plt.grid(True)
    plt.show()
