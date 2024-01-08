# -*- coding: utf-8 -*-
"""
    Author: tccuong1404
    Created on 2023-12-17
"""

import pymongo
from entity import post_entity
from entity import comment_entity


DATABASE_NAME = "crawler"
POST_COLLECTION = "posts"
COMMENT_COLLECTION = "comments"


def _cursor_to_list(cursor, mapper) -> list:
    res = []
    for row in cursor:
        ent = mapper(row)
        res.append(ent)
    return res


def get_post_collection(client: pymongo.MongoClient) -> pymongo.collection.Collection:
    collection = client.get_database(DATABASE_NAME).get_collection(POST_COLLECTION)
    return collection


def insert_post(client: pymongo.MongoClient, post: post_entity.PostEntity):
    platform = post.platform
    post_id = post.platform_post_id
    if get_post_by_post_id(client, platform, post_id) is not None:
        return
    
    collection = get_post_collection(client)
    collection.insert_one(post.__dict__)


def delete_post_by_post_id(client: pymongo.MongoClient, platform: str, post_id: str):
    collection = get_post_collection(client)
    collection.delete_one({"platform": platform, "platform_post_id": post_id})


def get_post_by_post_id(client: pymongo.MongoClient, platform: str, post_id: str) -> post_entity.PostEntity:
    collection = get_post_collection(client)
    result = collection.find_one({"platform": platform, "platform_post_id": post_id})
    return post_entity.from_dict(result)


def get_all_posts(client: pymongo.MongoClient, platform: str) -> list:
    collection = get_post_collection(client)
    cursor = collection.find({"platform": platform})
    return _cursor_to_list(cursor, post_entity.from_dict)

# =========================================
# =========== COMMENT SECTION =============

def get_comment_collection(client: pymongo.MongoClient) -> pymongo.collection.Collection:
    collection = client.get_database(DATABASE_NAME).get_collection(COMMENT_COLLECTION)
    return collection


def insert_comment(client: pymongo.MongoClient, comment: comment_entity.CommentEntity):
    post_id = comment.post_id
    if get_comment_by_comment_id(client, post_id, comment.comment_id) is not None:
        return
    
    collection = get_comment_collection(client)
    collection.insert_one(comment.__dict__)


def get_comment_by_comment_id(client: pymongo.MongoClient, post_id: str, 
                              comment_id: str) -> post_entity.PostEntity:
    collection = get_comment_collection(client)
    result = collection.find_one({"post_id": post_id, "comment_id": comment_id})
    return comment_entity.from_dict(result)


def get_comments_by_keyword(client: pymongo.MongoClient, keyword: str) -> list:
    pipeline = [
        {
            "$lookup": {
                "from": POST_COLLECTION,
                "localField": "post_id",
                "foreignField": "_id",
                "as": "post"
            }
        },
        {
            "$match": {
                "post.search_keyword": keyword
            }
        }
    ]

    cursor = get_comment_collection(client).aggregate(pipeline)
    return _cursor_to_list(cursor, comment_entity.from_dict)
    


def get_all_comments(client: pymongo.MongoClient) -> list:
    collection = get_comment_collection(client)
    cursor = collection.find()
    return _cursor_to_list(cursor, comment_entity.from_dict)