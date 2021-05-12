import json, hmac, hashlib, time, requests, base64, yaml, pprint, os

from cbpro import AuthenticatedClient, PublicClient
from itertools import islice

from ..common.provider import Provider
from ..common.auth import AuthenticationBase
from ..common.account import CryptoAccount
from ..common.portfolio import Portfolio

class CoinbaseClient(Provider):

    PROVIDER_ID = 'coinbase'

    def __init__(self):
        super(CoinbaseClient,self).__init__()
        
        self.public_client = PublicClient()

        api_key = self.settings['api_key']
        secret = self.settings['api_secret']
        passphrase = self.settings['api_pass']
        api_url = self.settings['api_url']

        if api_key and secret and passphrase and api_url:

            auth_client =  AuthenticatedClient(
                api_key,
                secret, 
                passphrase,
                api_url=api_url)

            if auth_client:
                self.auth_client = auth_client
            else:
                return Exception("Error while loading the authenticated client")

        self._load_accounts()

    #TODO: move to provider in general form when have more than 1 provider enabled
    @property
    def accounts(self):
        accounts_snapshot = []
        for account in self._accounts:
            price = self.get_current_price(account)
            snapshot = account.snapshot(price=price)
            accounts_snapshot.append(snapshot)
        return accounts_snapshot

    def _load_accounts(self):
        try:
            accounts = self.auth_client.get_accounts()
            valid_accounts = []
            for record in accounts:
                if "balance" not in record:
                    return Exception("Expecting balance field from account record")
                
                if float(record["balance"]) > 0:
                    crypto_account = CryptoAccount(record)
                    valid_accounts.append(crypto_account)

        except Exception as e:
            return Exception("Error while loading accounts", e)
        finally:
            self._accounts = valid_accounts
    
    def get_current_price(self,account):
        product_id = account.alias.upper()     
        if product_id != 'USD-USD':
            ticker = self.get_ticker(product_id)
            price = ticker['price'] 
            if type(price) != float:
                price = float(price)
        else:
            price = 1 

        return price

    def get_account_history(self, account):
        account_history = islice(self.auth_client.get_account_history(account.id), 300)
        history = list(account_history)

        for h in history:
            
            details = h["details"] 
            add_fields = {}

            for key, value in details.items():
                add_fields[key] = value

            h.update(add_fields)
            h.pop("details")

        return history

    def get_all_accounts_history(self):
        all_history = []
        for account in self._accounts:
            history = self.get_account_history(account)
            all_history.append([ h for h in history ])
        return all_history        

    def get_fills(self, params: dict={}):
        try:
            if "product_id" in params:
                product_id = params["product_id"]
                fills = self.auth_client.get_fills(product_id=product_id)
            elif "order_id" in params:
                order_id = params["order_id"]
                fills = self.auth_client.get_fills(order_id=order_id)   
            else:
                return Exception("Missing required paramaters product_id or order_id")

            if fills:
                return fills
            else:
                return Exception("Error while trying to load all accounts fills")

        except Exception as e:
            return e

    def get_ticker(self,product_id):
        ticker = self.public_client.get_product_ticker(product_id=product_id)
        return ticker

class CoinbasePortfolio(Portfolio):

    def __init__(self):
        super(CoinbasePortfolio,self).__init__(CoinbaseClient, name = "coinbase")
        self.load_accounts()

    # Could be moved to CoinbaseProvider
    @property 
    def current_snapshot(self):
        accounts = self.client.get_accounts()

        if accounts:          
            return accounts
        else:
            return Exception("Error while loading Coinbase accounts")
    
    def total_fees(self, time_range: dict):
        accounts = self.accounts
        total_fees = []
        if accounts:
            for account in accounts:
                for history in account.history:
                 
                    if history['type'] == 'fee':
                        fee_amount = float(history['amount']) * -1
                    
                        fee_amount = fee_amount * account.price 

                        total_fees.append(fee_amount)

            return total_fees
        else:
            return Exception("Error loading Coinbase accounts")
    
    def get_all_fills(self):
        fills = self.client.get_all_fills()
        print("All Fills:",fills)
        self.all_fills = list(fills)

    def get_fills_for_product_id(self,product_id):
        params = {
            "product_id": product_id
        }
        product_id_fills = self.client.get_fills(params=params)
        return product_id_fills



            
