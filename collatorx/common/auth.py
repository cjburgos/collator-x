import json, hmac, hashlib, time, requests, base64, pprint, os

from requests.auth import AuthBase

class AuthenticationBase(AuthBase):
    def __ini__(self, api_key, secret_key, api_pass):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_pass = api_pass
