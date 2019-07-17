# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class DoubanPipeline(object):
#     def process_item(self, item, spider):
#         return item

import json
import pymongo
import time
from scrapy.conf import settings
class DoubanPipeline(object):

# 将数据保存到mogodb
    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings['MONGODB_PORT']
        dbname=settings['MONGOOB_DBNAME']
        table = settings['MONGODB_TABLE']

        # 创建数据库连接
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[table]


    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item
