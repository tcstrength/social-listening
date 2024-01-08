# -*- coding: utf-8 -*-
"""
    Author: tccuong1404
    Created on 2023-12-17
"""

from datetime import datetime

STATUS_INSERT = 0
STATUS_RUNNING = 1
STATUS_COMPLETED = 2
PLATFORM_FACEBOOK = "facebook"

class PostEntity():
    def __init__(self, platform: str = None, search_keyword: str = None, post_id: int = None):
        dt = int(datetime.now().timestamp())
        self.platform = platform
        self.platform_post_id = post_id
        self.search_keyword = search_keyword
        self.crawl_status = STATUS_INSERT
        self.updated_date = dt
        self.created_date = dt


def from_dict(data: dict) -> PostEntity:
    if data is None:
        return None
    
    post = PostEntity()
    post.__dict__ = data
    return post