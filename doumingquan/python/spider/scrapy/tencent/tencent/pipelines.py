# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
import time
class TencentPipeline(object):
# 将数据保存到json中
    # def __init__(self):
    #     self.filename = open('tecent.json', 'wb+')
    #
    # def process_item(self, item, spider):
    #     jsontext = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #     self.filename.write(jsontext.encode("utf-8"))
    #     return item
    #
    # def close_spider(self, spider):
    #     self.filename.close()

# 将数据保存到数据库中(同步写法)
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='root', db="dishes")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = "insert into tencent(positionName,positionLink,positionType,peopleNum,workLocation,publishTime,catch_time) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(insert_sql, (item['positionName'], item['positionLink'], item['positionType'], item['peopleNum'],item['workLocation'],item['publishTime'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

# 异步的保存到数据库可以参照下文：https://www.cnblogs.com/attitudeY/p/7266331.html

