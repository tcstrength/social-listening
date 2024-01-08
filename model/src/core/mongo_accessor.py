# -*- coding: utf-8 -*-
"""
    Author: tccuong1404
    Created on 2023-12-17
"""

import pymongo
from urllib.parse import quote_plus


def get_mongo_uri(conf: dict) -> str:
    uri = "mongodb+srv://%s:%s@%s?retryWrites=true&w=majority" % (
        quote_plus(conf["user"]),
        quote_plus(conf["password"]),
        conf["host"])
        
    return uri


def create_mongo_client(conf: dict) -> pymongo.MongoClient:
    uri = get_mongo_uri(conf)
    client = pymongo.MongoClient(uri)
    return client