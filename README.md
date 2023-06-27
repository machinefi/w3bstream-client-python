# w3bstream-client-python

The Python Client for W3bstream integration on server

## Getting started

Install `w3bstream-client-python` via pip
``` shell
pip install w3bstream-client-python
```


## Example Code

``` py
from w3bstream_client_python import Client

# the endpoint and api_key are obtained on W3bstream-Studio
client = Client("endpoint", "api_key") 
# device_id is the identity for the device, and data is the data from the device. 
# data can be an empty string if served as a heartbeat
rsp = client.push_data("device_id", "data")
print(rsp.text)
```