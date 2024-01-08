# -*- coding: utf-8 -*-
"""
    Author: tccuong1404
    Created on 2023-12-17
"""

import os
import pytz

def get_login_script_path():
    return "./res/facebook_login_script.js"


def get_secrets_path():
    return "./res/secrets.yaml"


def get_timezone():
    return pytz.timezone("Asia/Ho_Chi_Minh")