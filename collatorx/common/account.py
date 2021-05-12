from uuid import uuid4
from datetime import datetime,timedelta

from .asset import BaseAsset, CryptoAsset


class BaseAccount():

    ACCOUNT_TYPE = 'base'

    def __init__(self):
        self._id = uuid4()
        self.asset = BaseAsset
        self._created_at = datetime.timestamp(datetime.now())
        self._modified_at = None

    @property
    def id(self):
        return self._id
    
    @property
    def created_at(self):
        return self._created_at
    
    @property
    def modified_at(self):
        return self._modified_at

    @property
    def account_type(self):
        return self.ACCOUNT_TYPE
    
    @modified_at.setter
    def _timestamp(self):
        self._modified_at = datetime.timestamp(datetime.now)   

class CryptoAccount(BaseAccount):

    ACCOUNT_TYPE = 'crypto'

    def __init__(self,record):
        super(CryptoAccount, self).__init__()

        if type(record) == dict:
            account_id = record['id']
            balance = record['balance']
            symbol = record['currency']
            available = record['available']
            hold = record['hold']
        elif type(record) == object:
            account_id = record.id
            balance = record.balance
            symbol = record.symbol
            available = record.available
            hold = record.hold
        else:
            raise Exception("Record datatype not recognized")

        balance = balance if type(balance) == float else float(balance)
        available = available if type(available) == float else float(available)
        hold = hold if type(hold) == float else float(hold)
        
        if account_id and account_id != '':
            self._id = account_id
            self._lock = True
        else:
            raise Exception("Account ID is missing")

        #Re-write to assign correct asset
        self.asset = CryptoAsset(symbol=symbol)

        #analgous to product id for Coinbase
        self.alias = f'{symbol.upper()}-USD'
        self.balance = balance
        self.available = available
        self.hold = hold
  
    def snapshot(self, price: float = 1):
        try:
            snapshot = {
                    "account_id": self.id,
                    "created_at": self.created_at,
                    "modified_at": self.modified_at,
                    "symbol": self.asset.symbol,
                    "type": self.account_type,
                    "balance": self.balance,
                    "alias": self.alias.lower(),
                    "asset_market_price": price,
                    "current_dollar_value": price * self.balance
                }
            return snapshot
        except Exception as e:
            print("Snapshot failed with message:{}".format(e))
                    