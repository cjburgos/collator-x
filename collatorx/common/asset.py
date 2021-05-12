from datetime import datetime
from uuid import uuid4

def load_record(record):
    if type(record) == dict:
        account_id = record['account_id']
        balance = record['balance']
        price = record['price']
    elif type(record) == object:
        account_id = record.account_id
        balance = record.balance
        price = record.price
    else:
        raise Exception("Account record datatype not recognized")

    balance if type(balance) == float else float(balance)
    price if type(price) == float else float(price)

    dollar_value = balance * price

    account = {
        "account_id":account_id,
        "balance":balance,
        "price":price,
        "dollar_value":dollar_value,
        "timestamp":datetime.timestamp(datetime.now())
    }   

    return account

class BaseAsset(object):

    ASSET_TYPE = 'default'

    def __init__(self):
        self._id = uuid4()
        self._dob = datetime.today()

    @property
    def asset_id(self):
        return str(self._id)

    @property
    def dob(self):
        return self._dob.isoformat()

    @property
    def type(self):
        return self.ASSET_TYPE

class CryptoAsset(BaseAsset):

    ASSET_TYPE = 'crypto'

    def __init__(self,symbol):
        super(CryptoAsset,self).__init__()
        self.symbol = symbol