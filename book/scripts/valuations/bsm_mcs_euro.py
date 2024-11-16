"""
Monte Carlo valuation of European call option in Black-Scholes-Merton model.

Python for Finance, 2nd ed.
(c) Dr. Yves J. Hilpisch

@author Preston Mackert
"""

# ------------------------------------------------------------------------------------------------------- #
# libraries
# ------------------------------------------------------------------------------------------------------- #

import math
import numpy as np


# ------------------------------------------------------------------------------------------------------- #
# parameter values
# ------------------------------------------------------------------------------------------------------- #

S0 = 100. # initial index level
K = 105. # strike price
T = 1.0 # time-to-maturity
r = 0.05 # riskless short rate
sigma = 0.2 # volatility

I = 100000 # number of simulations


# ------------------------------------------------------------------------------------------------------- #
# valuation algorithm
# ------------------------------------------------------------------------------------------------------- #

# pseudo-random numbers
z = np.random.standard_normal(I)
# index values at maturity
ST = S0 * np.exp((r - sigma ** 2 / 2) * T + sigma * math.sqrt(T) * z)
hT = np.maximum(ST - K, 0)
C0 = math.exp(-r * T) * np.mean(hT)


# ------------------------------------------------------------------------------------------------------- #
# result
# ------------------------------------------------------------------------------------------------------- #

print('Value of the European call option: %5.3f.' % C0)