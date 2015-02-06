#!/usr/bin/env python
# -*- coding:utf-8 -*-

# IG API Trader

import json
import time
import argparse

import yaml
import requests

import ig_markets.stream_client as igls


# Tell the user when the Lighstreamer connection state changes
def on_state(state):
    print 'New state:', state
    igls.LOG.debug('New state: ' + str(state))


# Process a lighstreamer price update
def processPriceUpdate(itemid, epic, myUpdateField):
    print "[%s] price update = " % epic + str(myUpdateField)


# Process an update of the users trading account balance
def processBalanceUpdate(itemid, myUpdateField):
    print "balance update = " + str(myUpdateField)


def test_stream_service(config_file="demo.yaml"):
    """Test IG stream service"""

    ystream = file(config_file, 'r')
    config = yaml.load(ystream)

    headers = {'content-type': 'application/json; charset=UTF-8',
               'Accept': 'application/json; charset=UTF-8',
               'X-IG-API-KEY': config['api_key']}

    payload = {'identifier': config['username'],
               'password': config['password']}

    url = config['api_url'] + "/session"
    r = requests.post(url, data=json.dumps(payload), headers=headers)

    cst = r.headers['cst']
    xsecuritytoken = r.headers['x-security-token']
    fullheaders = {'content-type': 'application/json; charset=UTF-8',
                   'Accept': 'application/json; charset=UTF-8', 'X-IG-API-KEY': config['api_key'],
                   'CST': cst, 'X-SECURITY-TOKEN': xsecuritytoken }

    body = r.json()
    lightstreamerEndpoint = body[u'lightstreamerEndpoint']
    clientId = body[u'clientId']
    accounts = body[u'accounts']

    # Depending on how many accounts you have with IG the '0' may need
    # to change to select the correct one (spread bet, CFD account etc)
    accountId = accounts[0][u'accountId']

    client = igls.LsClient(lightstreamerEndpoint+"/lightstreamer/")
    client.on_state.listen(on_state)
    client.create_session(username=accountId, password='CST-'+cst+'|XST-'+xsecuritytoken, adapter_set='')

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
                              item_ids='ACCOUNT:'+accountId,
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

