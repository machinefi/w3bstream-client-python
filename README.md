# w3bstream-client-python

The Python Client for W3bstream integration on server

## Getting started

Install `w3bstream-client-python` via pip
``` shell
pip install w3bstream-client-python
```


## Example Code

### Publish Event

``` py
from w3bstream_client_python import Client

# the endpoint and api_key are obtained on W3bstream-Studio
client = Client("endpoint", "api_key")
# event_type is the type of the event 
# token is the token for the device
# device_id is the identity for the device, and data is the data from the device. 
# data can be an empty string if served as a heartbeat
header = Header('event_type', b'token', 'device_id', datetime.datetime.now())
rsp = client.publish_event_sync(header, b'data')
print(rsp.text)
```

### Publish Event Async

``` py
client = Client('endpoint', 'api_key')
header = Header('event_type', b'token', 'device_id', datetime.datetime.now())

# async request
async def send():
    resp = await client.publish_event(header, b'hello world')
    print(await resp.text())

asyncio.run(send())

# batch async request
async def batch_send():
    tasks = [client.publish_event(header, b'hello world'), client.publish_event(header, b'hello world2')]
    responses = await asyncio.gather(*tasks)
    for response in responses:
        print(await response.text())

asyncio.run(batch_send())
```