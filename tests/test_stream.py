#!/usr/bin/env python
# -*- coding:utf-8 -*-

# IG Lightstream API test

import time
import argparse
import yaml

import ig_markets.stream_client as igls


# Tell the user when the Lighstreamer connection state changes
def on_state(state):
    print 'New state:', state
    igls.LOG.debug('New state: ' + str(state))


# Process a lighstreamer price update
def processPriceUpdate(itemid, myUpdateField, epic):
    print "[%s] price update" % epic + str(myUpdateField)


# Process an update of the users trading account balance
def processBalanceUpdate(itemid, myUpdateField):
    print "balance update = " + str(myUpdateField)


def test_stream_service(config_file="demo.yaml"):
    """Test IG stream service"""

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

    priceTable = igls.Table(client,
                            mode=igls.MODE_MERGE,
                            item_ids='L1:IX.D.DAX.IMF.IP',
                            schema='UPDATE_TIME BID OFFER CHANGE CHANGE_PCT MARKET_STATE',
                            item_factory=lambda row: tuple(float(v) for v in row))

    priceTable.on_update.listen(processPriceUpdate)

    balanceTable = igls.Table(client,
                              mode=igls.MODE_MERGE,
                              item_ids='ACCOUNT:' + account_id,
                              schema='PNL DEPOSIT AVAILABLE_CASH',
                              item_factory=lambda row: tuple(str(v) for v in row))

    balanceTable.on_update.listen(processBalanceUpdate)

    while True:
        time.sleep(10)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config',
                        help='YAML configuration file',
                        default='demo.yaml',
                        )
    args = parser.parse_args()
    test_stream_service(args.config)

