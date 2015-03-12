## IG Markets Clients (REST/Stream) - Python Library
----------------------------------------------------

A lightweight Python library that can be used to connect to the IG Markets REST and Stream APIs with a LIVE or DEMO account.

You can use the IG Markets HTTP / REST API to submit trade orders, open positions, close positions and view market sentiment.

You can use the IG Markets STREAM API to get realtime price, balance...

IG Markets provide Retail Spread Betting and CFD accounts for trading Equities, Forex, Commodities, Indices and much more.

Full details about the API along with information about how to open an account with IG can be found at the link below:

[http://labs.ig.com/](http://labs.ig.com/)

Heavily based on Lewis Barber (https://github.com/lewisbarber/ig-markets-rest-api-python-library) and 
femtotrader (https://github.com/femtotrader/ig-markets-stream-api-python-library) works.

Configuration
-------------

You can find an example configuration file in the tests directory (demo.yaml) and modify it with your account information.

```yaml
username: USERNAME
password: PASSWORD
api_key: API_KEY
api_url: https://demo-api.ig.com/gateway/deal
acc_number: ABC123
```

How To Use The REST Library
---------------------------

Using this library to connect to the IG Markets API is extremely easy. All you need to do is import the IGRestClient class, create an instance, and call the methods you wish to use. 
There is a method for each endpoint exposed by their API.
The code sample below shows you how to connect to the API and retrieve all open positions for the active account.

**Note:** The secure session with IG is established when you create an instance of the IGRestClient class.

```python
import yaml

from rest_client import IGRestClient

stream = file('demo.yaml', 'r')
config = yaml.load(stream)

ig_service = IGRestClient(config['username'],
                          config['password'],
                          config['api_key'],
                          config['api_url'])

ig_service.create_session()

open_positions = ig_service.fetch_open_positions()
print(open_positions)
```


How To Use The Stream Library
-----------------------------

Using this library to connect to the IG Markets API is extremely easy.

More details on schema and available streams at : http://labs.ig.com/streaming-api-guide

Note: on a normal account, you're limited to 40 simultaneous subscriptions per connection.

Example code:


```python
import yaml

import ig_markets.stream_client as igls

# Tell the user when the Lighstreamer connection state changes
def on_state(state):
    print 'New state:', state
    igls.LOG.debug('New state: ' + str(state))


# Process a lighstreamer price update
def processPriceUpdate(itemid, myUpdateField, epic):
    print "[%s] price update" % epic + str(myUpdateField)


ystream = file(config_file, 'r')
config = yaml.load(ystream)

client = igls.IGLsClient()
client.on_state.listen(on_state)
account_id = client.create_session(username=config['username'],
                                   password=config['password'],
                                   api_url=config['api_url'],
                                   api_key=config['api_key'])

priceTable = igls.Table(client,
                        mode=igls.MODE_MERGE,
                        item_ids='L1:CS.D.EURUSD.CFD.IP',
                        schema='UPDATE_TIME BID OFFER CHANGE CHANGE_PCT MARKET_STATE',
                        item_factory=lambda row: tuple(float(v) for v in row))

priceTable.on_update.listen(processPriceUpdate)
```

