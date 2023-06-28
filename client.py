import requests
import aiohttp
import datetime
from typeguard import typechecked

@typechecked
class Header:
    def __init__(self, event_type: str, token: bytes, device_id: str, timestamp: datetime.datetime):
        self.event_type = event_type
        self.token = token
        self.device_id = device_id
        self.timestamp = timestamp

@typechecked
class Client:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

    # TODO: support publish_event non-blocking, which can send data async in batch
    # TODO: make publish_event non-panic
    def publish_event(self, header: Header, payload: bytes):
        headers = {
            'Authorization': 'Bearer ' + self.api_key,
        }
        body = [{
            'device_id': header.device_id,
            'event_type': header.event_type,
            'payload': payload.decode('utf-8'),
            'timestamp':  int(round(header.timestamp.timestamp())),
        }]
        return requests.post(
            self.endpoint, json=body, headers=headers)
