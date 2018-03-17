# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from pymongo import MongoClient
import json
import time
import os
from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors



# 自定义插件

class CheckPipeline(object):
    """ 去除空值 """
    def process_item(self, item, spider):
        for key in item:
            if item[key] is None:
                raise DropItem('%s is missing %s' % (item, key))
        return item

class MongoDBPipeline(object):
    """MongoDB管道 
    """

    def process_item(self, item, spider):
        """ 插入数据 """
        postItem = dict(item)  
        self.conn.insert(postItem)  
        return item  
    
    def open_spider(self, spider):
        """ 在爬虫打开的时候开启数据库链接"""
        self.client = MongoClient(host=settings['MONGODB_SERVER'], port=settings['MONGODB_PORT'])
        if settings['MONGODB_USER'] and settings['MONGODB_PASSWORD']:
            self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings['MONGODB_DB']]  # 获得数据库的句柄
        self.conn = self.db[settings['MONGODB_COLLECTION']]  # 获得collection的句柄

    def close_spider(self, spider):
        """ 在爬虫关闭的时候关闭数据库链接 """
        self.client.close()


class JsonWriterPipeline(object):
    """Json管道
    """

    def open_spider(self, spider):
        file_name = settings["JSON_FOLDER"]+ str(spider.name)+str(time.time()).replace(".", "")+".json"
        self.file = open(file_name, "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item 
    
        
class MySQLTwistedPipeline(object):
    
    def __init__(self,dbpool):
        self.dbpool = dbpool
    #从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DB_NAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入编程异步执行
        #第一个参数是我们定义的函数
        self.dbpool.runInteraction(self.do_insert,item)
        #错误处理

    def do_insert(self,cursor,item):
        #执行具体的插入
        insert_sql = """
                    insert into quotes_follow(text,author) VALUES (%s,%s)
                    """
        cursor.execute(insert_sql, (item['text'], item['author']))



        

        
