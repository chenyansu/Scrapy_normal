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

    # def __init__(self):
    #     dbparms = dict(
    #         host = settings["MYSQL_HOST"],
    #         db = settings["MYSQL_DB_NAME"],
    #         user = settings["MYSQL_USER"],
    #         passwd = settings["MYSQL_PASSWORD"],
    #         charset='utf8',
    #         cursorclass=pymysql.cursors.DictCursor,
    #         use_unicode=True,
    #     )
    #     self.dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

    def process_item(self, item, spider):
        """使用twisted将mysql插入变成异步执行"""
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider) #处理异常
        return item

    def handle_error(self, e):
        log.err(e)

    def do_insert(self, cursor,item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        item_value_list = []
        for i in self.item_key_list:
            item_value_list.append(item[i]) # 循环获取键值
        params = tuple(item_value_list)
        cursor.execute(self.insert_sql, params) 

    def open_spider(self, item, spider):

        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DB_NAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        """ 生成sql指令 """
        table_name = spider.name
        part1 = "insert into "
        part2 = table_name
        part3 = "("
        self.item_key_list= [] ##### 键列表 ####
        for k in item.keys():
            self.item_key_list.append(k)
        part4 = str(self.item_key_list.item_key_list).replace("[", "").replace("]", "")
        part5 = ") Values ("
        for s in range(len(item)):
            part5 += "%s, "
        part6 = ")"
        self.insert_sql = part1+part2+part3+part4+part5+part6 ### mysql insert指令 ###



    def close_spider(self, item, spider):\
        return item
        
        

        
