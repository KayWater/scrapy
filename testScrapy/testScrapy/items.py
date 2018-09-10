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
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class TagItem(scrapy.Item):
    name = scrapy.Field()
    
class AuthorItem(scrapy.Item):
    name = scrapy.Field()
    birthdate = scrapy.Field()
    birthplace = scrapy.Field()
    description = scrapy.Field()
        