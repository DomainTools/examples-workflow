import hashlib
import hmac
from datetime import *

class HmacSignatureGenerator:
    def __init__(self, api_username, api_key):
        self.api_username = api_username
        self.api_key = api_key

    def create_iso8601_timestamp(self):
        return datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def generate_signature(self, uri):
        timestamp = self.create_iso8601_timestamp()
        params = ''.join([self.api_username, timestamp, uri])
        signature = hmac.new(self.api_key.encode('utf-8'), params.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        return signature, timestamp



