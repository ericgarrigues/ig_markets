#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run unit tests using
nosetests -s -v
"""

import yaml
import argparse
import pandas as pd

from ig_markets.rest_client import IGRestClient

def test_ig_service(config='demo.yaml'):

    stream = file(config, 'r')
    config = yaml.load(stream)

    ig_service = IGRestClient(config['username'],
                              config['password'],
                              config['api_key'],
                              config['api_url'])

    ig_service.create_session()

    print("fetch_accounts")
    response = ig_service.fetch_accounts()
    print(response)
    assert(response['balance'][0]['available']>0)

    print("fetch_account_activity_by_period")
    response = ig_service.fetch_account_activity_by_period(10000)
    print(response)
    assert(isinstance(response, pd.DataFrame))

    print("fetch_account_activity_by_period")
    response = ig_service.fetch_account_activity_by_period(10000)
    print(response)
    assert(isinstance(response, pd.DataFrame))

    print("fetch_transaction_history_by_type_and_period")
    response = ig_service.fetch_transaction_history_by_type_and_period(10000, "ALL")
    print(response)
    assert(isinstance(response, pd.DataFrame))

    print("fetch_open_positions")
    response = ig_service.fetch_open_positions()
    print(response)
    assert(isinstance(response, pd.DataFrame))

    print("fetch_working_orders")
    response = ig_service.fetch_working_orders()
    print(response)
    assert(isinstance(response, pd.DataFrame))

    print("fetch_top_level_navigation_nodes")
    response = ig_service.fetch_top_level_navigation_nodes()
    print(response) # dict with nodes and markets
    assert(isinstance(response, dict))
    market_id = response['nodes']['id'].iloc[0]

    print("fetch_client_sentiment_by_instrument")
    response = ig_service.fetch_client_sentiment_by_instrument(market_id)
    print(response)
    assert(isinstance(response, dict))

    print("fetch_related_client_sentiment_by_instrument")
    response = ig_service.fetch_related_client_sentiment_by_instrument(market_id)
    print(response)
    assert(isinstance(response, pd.DataFrame))

    print("fetch_sub_nodes_by_node")
    node = market_id #?
    response = ig_service.fetch_sub_nodes_by_node(node)
    print(response)

    print("fetch_all_watchlists")
    response = ig_service.fetch_all_watchlists()
    print(response)
    watchlist_id = response['id'].iloc[0]
    #epic = 

    print("fetch_watchlist_markets")
    response = ig_service.fetch_watchlist_markets(watchlist_id)
    print(response)
    epic = response['epic'].iloc[0]

    print("fetch_market_by_epic")
    response = ig_service.fetch_market_by_epic(epic)
    print(response)

    print("search_markets")
    search_term = 'UNDEF'
    response = ig_service.search_markets(epic)
    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('config',
                        help='YAML configuration file',
                        default='demo.yaml',
                        )
    args = parser.parse_args()
    test_ig_service(args.config)
