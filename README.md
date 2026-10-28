# Black-Scholes Option Pricer

Implementation of the Black-Scholes model for pricing European options with real market data analysis.

## Features
- Call and put pricing using Black-Scholes formula
- Greeks calculation (Delta, Gamma, Theta, Vega, Rho)
- Implied volatility using bisection method
- Volatility skew visualization vs historical volatility using live AAPL options data

## Requirements
pip install numpy scipy matplotlib yfinance

## Usage
python Black_scholes.py

## Binomial Tree Pricer
- Implements Cox-Ross-Rubinstein (CRR) binomial tree
- Demonstrates convergence to Black-Scholes as number of steps N → ∞
- Verified: N=1000 steps gives price within 0.0003 of analytical BS price

## Delta Hedging Simulation
- Simulates delta hedging a short call position over 30 days
- Stock price path generated using Geometric Brownian Motion (GBM)
- Rebalances delta daily using Black-Scholes delta (N(d1))
- Runs 1000 simulations to show P&L distribution
- Result: Mean P&L ≈ $0, confirming Black-Scholes price is the exact cost of hedging