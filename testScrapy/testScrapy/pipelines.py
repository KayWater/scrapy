# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from testScrapy import settings
from testScrapy.items import AuthorItem, TagItem

class TestscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class QuotePipeline(object):
    
    def __init__(self):
        self.connection = pymysql.connect(
            host = self.settings.MYSQL_HOST,
            user = self.settings.MYSQL_USER,
            password = self.settings.MYSQL_PASSWORD,
            database = self.settings.MYSQL_DB)
        
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        pass
    
class AuthorPipeline(object):
    
    def __init__(self):
        self.connection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            database = settings.MYSQL_DB)
        
        self.cursor = self.connection.cursor()
        
    def process_item(self, item, spider):
        if isinstance(item, AuthorItem): 
            sql = "insert into author (name, birthdate, birthplace, description) values (%(name)s, %(birthdate)s, %(birthplace)s, %(description)s)"
            self.cursor.execute(sql, dict(item))
            self.connection.commit()
        return item       
    
class TagPipeline(object):
    
    def __init__(self):
        self.connection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            database = settings.MYSQL_DB)
        
        self.cursor = self.connection.cursor()
        
    def process_item(self, item, spider): 
        if isinstance(item, TagItem):
            sql = "insert into tag (name) values (%(name)s)"
            result = self.cursor.execute(sql, dict(item))
            self.connection.commit()
        return item
    
    
    