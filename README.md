# w3bstream-client-python

The Python Client for W3bstream integration on server

## Getting started

Install `w3bstream-client-python` via `pip3`
``` shell
pip3 install w3bstream-client-python
```


## Example Code

### Publish Event Synchronously

``` py
from w3bstream_client_python import Client, Header

# the http_route, project and api_key are obtained on W3bstream-Studio
client = Client("http_route", "api_key")
# device_id is the identity for the device
# payload can be an empty string if served as a heartbeat
header = Header('device_id')
rsp = client.publish_event_sync(header, b'payload')
print(rsp.text)
```

### Publish Event Asynchronously

``` py
client.publish_event(header, b'payload')
```