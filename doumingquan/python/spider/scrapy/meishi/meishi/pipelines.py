# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import time
class TencentPipeline(object):

# 将数据保存到数据库中
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', passwd='root', db="dishes")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        insert_sql = "insert into foods(name,url,food,method,nutrient,hot_engery,fattiness,carbo,protein,choles,fibrin,mg,ca,fe,zn,mn,cu,k,catch_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cursor.execute(insert_sql, (item['name'],item['url'],item['food'],item['method'],item['nutrient'],item['hot_engery'],item['fattiness'],item['carbo'],item['protein'],item['choles'],item['fibrin'],item['mg'],item['ca'],item['fe'],item['zn'],item['mn'],item['cu'],item['k'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        self.conn.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
