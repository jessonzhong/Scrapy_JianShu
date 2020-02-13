# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['content'],
                                       item['author'], item['avatar'],
                                       item['pub_time'], item['origin_url'],
                                       item['article_id'], item['read_count'],
                                       item['like_count'], item['word_count'],
                                       item['subjects'], item['comment_count']))
        self.conn.commit()
        return item

    @property  # 属性操作，可直接调用
    def sql(self):
        if not self._sql:
            self._sql = '''insert into article(title,author,avatar,publish_time,article_id,
               origin_url,content) value(%s,%s,%s,%s,%s,%s,%s)'''
            return self._sql
        return self._sql


# 异步插入数据库
class JianshuTwistedPipeline(object):
    def __init__(self):
        params = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1326628437',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }
        # 调用异步连接池实现异步插入数据库
        self.dbpool = adbapi.ConnectionPool("pymysql", **params)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = '''insert into article(title,author,avatar,publish_time,article_id,
            origin_url,content) value(%s,%s,%s,%s,%s,%s,%s)'''
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # 异步插入数据
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 错误处理
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, item, cursor):
        cursor.execute(self.sql, (item['title'], item['author'], item['avatar'], item['publish_time'],
                                  item['article_id'], item['origin_url'], item['content']))

    def handle_error(self, item, error, spider):
        print('+' * 30 + 'error' + '+' * 30)
        print(error)
        print('+' * 30 + 'error' + '+' * 30)
