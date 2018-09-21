# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.exporters import JsonLinesItemExporter 
from testScrapy import settings
from testScrapy.items import AuthorItem, QuoteItem, IpsItem, MovieItem
from testScrapy.spiders import proxySpider, doubanSpider

class TestscrapyPipeline(object):
    def process_item(self, item, spider):
        return item

class QuotePipeline(object):
    
    def __init__(self):
        self.connection = pymysql.connect(
            host = settings.MYSQL_HOST,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            database = settings.MYSQL_DB)
        
        self.cursor = self.connection.cursor()
    
    def process_item(self, item, spider):
        if isinstance(item, QuoteItem):
            sql = "insert into quote (text, author, tags) values (%(text)s, %(author)s, %(tags)s)"
            self.cursor.execute(sql, dict(item))
            self.connection.commit()
        return item
    
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
    
class IpJsonPipeline(object):
    # export json file for scraped ip list
    
    # instance a file object and an JsonLinesItemExporter object 
    def open_spider(self, spider):
        file = open("../proxy.json", 'wb', encoding='utf-8')
        self.exporter = JsonLinesItemExporter(file)
        self.exporter.start_exporting()
    
    # close file object and finish exporting
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.exporter.file.close()
    
    # exporting item 
    def process_item(self, item, spider):
        if isinstance(item, IpsItem) and isinstance(spider, proxySpider.ProxySpider):
            self.exporter.export_item(item)
        return item
    
class MovieJsonPipeline(object):
    
    def open_spider(self, spider):
        if isinstance(spider, doubanSpider.DoubanSpider):
            file = open("../movies.json", 'wb')
            self.exporter = JsonLinesItemExporter(file, ensure_ascii=False)
            self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.exporter.file.close()
        
    def process_item(self, item, spider):
        if isinstance(item, MovieItem) and isinstance(spider, doubanSpider.DoubanSpider):
            self.exporter.export_item(item)
        return item   
      