# w3bstream-client-python


## Example Code

``` py
from w3bstream_client_python import Client

client = Client("endpoint", "api_key")
rsp = client.push_data("device_id", "data")
print(rsp.text)
```