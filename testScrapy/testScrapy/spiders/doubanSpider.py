'''
Created on 2018年9月12日

@author: iw12082
'''

import scrapy
from scrapy.spiders import CrawlSpider, Rule
import json
import random
from testScrapy.items import MovieItem
from scrapy.linkextractors import  LinkExtractor

class DoubanSpider(CrawlSpider):
    name = 'douban'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 5,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        'FEED_URI': 'file:///D:/123.json',
        'FEED_FORMAT': 'jsonlines',
        'COOKIES_ENABLED': False,
#        'IMAGES_STORE': '../images/',
 
    }
    allowed_domains = ['douban.com']
    start_urls = ['http://movie.douban.com']
    
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'/subject/\d+/', )), callback='parse_movie', process_links='strip_query_string' ),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r'/celebrity/\d+/', )), callback='parse_celebrity'),
    )
            
    def parse_movie(self, response):
        
        movie_item = MovieItem()
       
        title = response.xpath("//h1/span[@property='v:itemreviewed']/text()").extract_first()
        year = response.css("h1 span.year::text").extract_first()
        mainpic_url = response.css("div.subject a.nbgnbg img::attr(src)").extract()
        
        
        directors = response.xpath("//div[@id='info']//a[@rel='v:directedBy']/@href").extract()
        
        screenwriters = response.xpath("//div[@id='info']").css("span.pl")[1].xpath("./following-sibling::span/a/@href").extract()
        
        actors = response.xpath("//div[@id='info']//a[@rel='v:starring']/@href").extract()
        
        genre = response.xpath("//div[@id='info']//span[@property='v:genre']/text()").extract()
        
        region = response.xpath("//div[@id='info']").css("span.pl")[4].xpath("./following-sibling::text()").extract_first()
        
        movie_item['title'] = title
        movie_item['year'] = year
        movie_item['directors'] = directors
        movie_item['screenwriters'] = screenwriters
        movie_item['actors'] = actors
        movie_item['genre'] = genre
        movie_item['region'] = region
        yield movie_item
        
    def parse_celebrity(self, response):
        response
        pass
    
    def strip_query_string(self, request): 
        request
        pass 