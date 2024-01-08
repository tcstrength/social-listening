# -*- coding: utf-8 -*-
"""
    Author: tccuong1404
    Created on 2023-12-17
"""

from datetime import datetime


PLATFORM_FACEBOOK = "facebook"

class CommentEntity():
    def __init__(
        self, 
        post_id: str = None, 
        comment_id: int = None, 
        content: str = None, 
        comment_date: str = None
    ):
        dt = int(datetime.now().timestamp())
        self.post_id = post_id
        self.comment_id = comment_id
        self.content = content
        self.comment_date = comment_date
        self.updated_date = dt
        self.created_date = dt


def from_dict(data: dict) -> CommentEntity:
    if data is None:
        return None
    
    post = CommentEntity()
    post.__dict__ = data
    return post