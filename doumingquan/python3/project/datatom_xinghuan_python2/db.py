#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import logging
import psycopg2


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OperDb():
    def __init__(self):
        self.source_params()

    #连接源数据库
    def source_params(self):
        try:
            self.conn = psycopg2.connect(database="postgres", user="stork",password="stork", host="172.26.16.90", port="14103")
            if self.conn:
                self.cursor = self.conn.cursor()
                logger.info('The database has been successfully connected')
        except Exception as e:
            s = sys.exc_info()
            logger.error(s)
    
    #插入数据
    def exec_sql(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def select_sql(self, sql):
    	logger.info(sql)
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            return res
        except Exception as e:
            s = sys.exc_info()
            logger.error(s)
    def insert_sql(self,tableName,dataDict):
        columns = ','.join(dataDict.keys())
        value = ','.join(dataDict.values()).replace(',','\',\'')
        valuess = "'{value}'".format(value = value)
        sql = "insert into {tableName}({columns}) values({valuess})".format(tableName=tableName, columns=columns, valuess = valuess)
        logger.info(sql)
        self.exec_sql(sql)

    def update_sql(self,tableName,dataDict,whereDict):
        info = ""
        for key,value in dataDict.items():
            info += "{key}='{value}',".format(key=key, value=value)
        info = info[:-1]
        whereInfo = ""
        for key,value in whereDict.items():
            whereInfo += "{key}='{value}' and ".format(key=key, value=value)
        whereInfo = whereInfo[:-5]
        sql = "update  {tableName} set {info} where {whereInfo}".format(tableName=tableName, info=info, whereInfo=whereInfo)
        logger.info(sql)
        self.exec_sql(sql)
    
    def __del__(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
            logger.info("The database has been closed")
if __name__ == '__main__':
    sql = "insert into public.task_info values('sss','sss','ssss')"
    sql = "select * from public.task_info"
    dber = OperDb()
    #dber.select_sql(sql)
    tableName = 'sss.sss'
    dataDict = {'a':'aa','b':'bb'}
    whereDict = {'a':'aa','b':'bb'}
    dber.update_sql(tableName,dataDict,whereDict)

