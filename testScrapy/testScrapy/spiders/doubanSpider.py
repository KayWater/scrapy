'''
Created on 2018年9月12日

@author: iw12082
'''

import scrapy
import json
import random
from testScrapy.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 5,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        'FEED_URI': 'file:///D:/123.json',
        'FEED_FORMAT': 'jsonlines',
        'COOKIES_ENABLED': False,
        'IMAGES_STORE': '../images/',
        'DOWNLOAD_MIDDLEWARE': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100}
    }
    
    def start_requests(self):
        urls = ["https://movie.douban.com/top250"]
        ip = self.get_ip()
        for url in urls:
            
            yield scrapy.Request(url=url, meta={"proxy": "http://%s"%ip}, callback=self.parse)
            
    def parse(self, response):
        
        for link in response.css("div.info a::attr(href)"):
            yield response.follow(link, self.parse_movie)
        
        for link in response.css("div.paginator > a::attr(href)"):
            yield response.follow(link, self.parse)
            
    def parse_movie(self, response):
        
        url = response.url 
        
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
        
    def get_ip(self):
        with open("../validProxy.json", 'r') as f:
            text = f.readline()
            return text
        