import json
import requests
import datetime


class Client:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    # TODO: support push_data non-blocking, which can send data async in batch
    # TODO: make push_data non-panic
    def push_data(self, deviceID, data, event_type="DEFAULT"):
        self._validate_data_format(deviceID, data, event_type)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key,
        }
        body = [{
            'device_id': deviceID,
            'event_type': event_type,
            'payload': data,
            'timestamp':  int(round(datetime.datetime.now().timestamp())),
        }]
        return requests.post(
            self.endpoint, data=json.dumps(body), headers=headers)

    def _validate_data_format(self, deviceID, data, event_type):
        if type(deviceID) != str:
            raise ValueError("deviceID should be a string")
        if type(data) != str:
            raise ValueError("data should be a string")
        if type(event_type) != str:
            raise ValueError("event_type should be a string")
