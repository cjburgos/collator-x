import json, time, pprint


from datetime import datetime,timedelta
from typing import Mapping
from uuid import uuid4

from .provider import Provider

class Portfolio():
    def __init__(self, provider: Provider , name: str = 'default'):
        self._id = uuid4()
        self.name = name
        self.client = provider

    @property
    def id(self):
        return str(self._id)
    
    @property
    def name(self):
        return self.name