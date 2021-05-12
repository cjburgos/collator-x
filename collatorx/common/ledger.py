from datetime import datetime
from uuid import uuid4

class Ledger():
    
    LEDGER_TYPE = "default"

    def __init__(self):
        self._id = uuid4()
        self._dob = datetime.datetime.today()

    @property
    def ledger_id(self):
        return str(self._id)

    @property
    def genesis_date(self):
        return self._dob.isoformat()

