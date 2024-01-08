# -*- coding: utf-8 -*-
"""
    Author: tccuong1404
    Created on 2023-12-17
"""


import yaml
from core import env_manager


def load_secrets() -> dict:
    file_path = env_manager.get_secrets_path()
    
    with open(file_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        return data


def load_cookie():
    secrets = load_secrets()
    return secrets["cookie"]


def load_mongodb():
    secrets = load_secrets()
    return secrets["mongodb"]