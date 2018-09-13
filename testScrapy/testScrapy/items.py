# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QuoteItem(scrapy.Item):
    id = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class TagItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    
class AuthorItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    birthdate = scrapy.Field()
    birthplace = scrapy.Field()
    description = scrapy.Field()
        
class MovieItem(scrapy.Item):
    
    title = scrapy.Field()
    directors = scrapy.Field()
    screenwriters = scrapy.Field()
    actors = scrapy.Field()
    year = scrapy.Field()
    genre = scrapy.Field()
    region = scrapy.Field()
    summary = scrapy.Field()

class IpsItem(scrapy.Item):
    ip_list = scrapy.Field()