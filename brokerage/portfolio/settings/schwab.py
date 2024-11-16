"""
Charles Schwab API utility. This file is a settings/config file that houses classes to assist with using 
the Schwab REST APIs.

@author Preston Mackert
"""

# ------------------------------------------------------------------------------------------------------- #
# libraries
# ------------------------------------------------------------------------------------------------------- #

import os
import json
import time
import base64
import requests
import datetime
import pprint
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, date

# ------------------------------------------------------------------------------------------------------- #
# global application variables
# ------------------------------------------------------------------------------------------------------- #

# Load environment variables from .env
load_dotenv()
schwab_key = os.environ['schwab_key']
schwab_secret = os.environ['schwab_secret']
redirect_uri = os.environ['redirect_uri']

# ------------------------------------------------------------------------------------------------------- #
# authentication
# ------------------------------------------------------------------------------------------------------- #

class Authenticator:
    """
    This class manages an authenticated session into the Schwab API. It obtains an access 
    and refresh token from the oauth endpoint, with a given expiration date for the access token.
    Docs: https://beta-developer.schwab.com/user-guides/apis-and-apps/oauth-restart-vs-refresh-token
    """
    def __init__(self):
        self.base_url = 'https://api.schwabapi.com/v1/oauth/token'
        # default load these from file
        token_file = open('./settings/tokens.json')
        tokens = json.load(token_file)
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        # timer field that is controlled by update_tokens() function
        self.expiration = tokens['expiration']
    
    def get_auth_url(self):
        """ 
        Uses the app key to generate an auth url 
        """
        auth_url = f'https://api.schwabapi.com/v1/oauth/authorize?client_id={schwab_key}&redirect_uri={redirect_uri}'
        return auth_url
    
    def get_tokens(self, returned_link):
        """ 
        Uses a request to generate refresh and access tokens for managing an authentication session 
        """
        code = f"{returned_link[returned_link.index('code=')+5:returned_link.index('%40')]}@"
        headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(f'{schwab_key}:{schwab_secret}', 'utf-8')).decode('utf-8')}", 
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'authorization_code', 
            'code': code, 
            'redirect_uri': redirect_uri
        }
        response = requests.post(f'{self.base_url}', headers=headers, data=data).json()
        self.access_token = response['access_token']
        self.refresh_token = response['refresh_token']
        self.expiration = response['expires_in']
        # write to file - persist object
        tokens = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expiration': self.expiration
        }
        with open('./settings/tokens.json', 'w') as token_file:
            json.dump(tokens, token_file)
        self.refresh_timer()
        return response

    def update_tokens(self):
        """
        function that is called on the expiration timer to use a refresh token. Prevents continued need to access 
        the login micro-site used to obtain the first access token.
        """
        headers = {
            'Authorization': f"Basic {base64.b64encode(bytes(f'{schwab_key}:{schwab_secret}', 'utf-8')).decode('utf-8')}", 
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'refresh_token', 
            'redirect_uri': redirect_uri,
            'refresh_token': self.refresh_token
        }
        response = requests.post(f'{self.base_url}', headers=headers, data=data).json()
        self.access_token = response['access_token']
        self.refresh_token = response['refresh_token']
        self.expiration = response['expires_in']
        # write to file - persist object
        tokens = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expiration': self.expiration
        }
        with open('./settings/tokens.json', 'w') as token_file:
            json.dump(tokens, token_file)
        self.refresh_timer()
        return response
    
    def refresh_timer(self):
        """
        when a new lms workflow is finished or if a refresh token is applied, then this function automatically 
        keeps the access token rotated.
        """
        while self.expiration > 0:
            timer = datetime.timedelta(seconds = self.expiration)
            self.expiration = timer.seconds
            time.sleep(1)
            self.expiration -= 1
        self.update_tokens() 


# ------------------------------------------------------------------------------------------------------- #
# account details
# ------------------------------------------------------------------------------------------------------- #

class Account:
    """
    This class wraps the functions related to the Schwab account functions in the individual trader 
    api endpoint: https://api.schwabapi.com/trader/v1
    """
    def __init__(self, auth):
        self.auth = auth
        self.access_token = auth.access_token
        self.refresh_token = auth.refresh_token
        self.expiration = auth.expiration
        self.base_url = 'https://api.schwabapi.com/trader/v1/'
        
    def get_accounts(self):
        """ 
        obtains details for all accounts linked to the authenticated user 
        """
        accounts = requests.get(
            f'{self.base_url}/accounts', 
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        return accounts

    def get_account_numbers(self):
        """ 
        obtains account numbers for each account linked to the authenticated user 
        """
        account_numbers = requests.get(
            f'{self.base_url}/accounts/accountNumbers', 
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        return account_numbers

    def get_preferences(self):
        """ 
        obtains the logged-in user's preferences 
        """
        preferences = requests.get(
            f'{self.base_url}/userPreference', 
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        return preferences
        
    def get_account_detail(self, account_number):
        """ 
        obtains details for a specific account number that is linked to the authenticated user 
        """
        account_details = requests.get(
            f'{self.base_url}/accounts/{account_number}', 
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        return account_details
        
    def get_orders(self, start_date, end_date):
        """ 
        obtains all orders from an account in the specified date range 
        """
        order_details = requests.get(
            f'{self.base_url}/accounts/orders', 
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        return order_details


# ------------------------------------------------------------------------------------------------------- #
# market data
# ------------------------------------------------------------------------------------------------------- #

class Position:
    """
    A position encapsulates a single symbol that is part of the portfolio. This class wraps the functions 
    related to the Schwab market data functions in the individual trader api endpoint: 
    https://api.schwabapi.com/marketdata/v1
    """
    def __init__(self, auth, symbol):
        self.base_url = 'https://api.schwabapi.com/marketdata/v1/'
        self.access_token = auth.access_token
        self.symbol = symbol
        self.quantity = 0
        self.price = 0
        self.cost_basis = 0
        self.market_value = 0
        self.price_history = pd.DataFrame()
        
    def get_quotes(self):
        """ 
        obtains quotes from a given ticker 
        """
        quotes = requests.get(
            f'{self.base_url}/{self.symbol}/quotes', 
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        return quotes

    def get_price_history(self, start_date, end_date):
        """ 
        obtains the price history over a given interval of time for a symbol 
        
        parameters (need to figure out parameters still, not pulling in nightly):
          'symbol'*: {}
    
          'periodType': {-, day, month, year, ytd}
    
          'period': {1, 2, 3, 5, 6, 10, 15, 20}
              #The number of chart 'period' types. If the 'periodType' is:
              • day - [1, 2, 3, 4, 5, 10 - [default: 10]
              • month - [1, 2, 3, 6 - [default: 1]
              • year - [1, 2, 3, 5, 10, 15, 20 - [default: 1]
              • ytd - [1 - [default: 1]
    
          'frequencyType': {minute, daily, weekly, monthly}
              #The time 'frequencyType'. If the 'periodType' is:
              • day - [minute] - [default: minute]
              • month - [daily, weekly] - [default: weekly]
              • year - [daily, weekly, monthly] - [default: monthly]
              • ytd - [daily, weekly] - [default: weekly]
    
          'frequency': {1, 5, 10, 15, 30}
              #The time frequency duration If the frequencyType is:
              • minute - [1, 5, 10, 15, 30]
              • daily - [1]
              • weekly - [1]
              • monthly - [1]
              #If frequency is not specified, default value is 1.#
    
          'startDate': {}
              #Time in milliseconds since the UNIX epoch (eg 1451624400000)
              #If not specified startDate will be (endDate - period) - excluding weekends and holidays
    
          'endDate': {}
              #Time in milliseconds since the UNIX epoch (eg 1451624400000)
              #If not specified, the endDate will default to the market close of previous business day.
    
          'needExtendedHoursData': {true, false}
          'needPreviousClose': {true, false}    
        """
        price_history = requests.get( 
            f'{self.base_url}/pricehistory?symbol={self.symbol}&periodtype=day&\
            startdate={start_date}&enddate={end_date}',
            headers={'Authorization': f'Bearer {self.access_token}'}
        ).json()
        # convert to dataframe for continued analysis - datetime column is numpy.int64
        self.price_history = pd.json_normalize(price_history['candles']).dropna()
        self.price_history['datetime'] = pd.to_datetime(self.price_history['datetime'], unit='ms')
        return price_history

    def get_volatility(self, window=20):
        """ 
        obtains volatility on the price history 
        """
        self.price_history['log_ret'] = np.log(self.price_history['close']/self.price_history['close'].shift(1))
        self.price_history['volatility'] = self.price_history['log_ret'].rolling(252).std() * np.sqrt(252)
        return self.price_history
