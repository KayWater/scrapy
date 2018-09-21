'''
Created on 2018年9月12日

@author: iw12082
'''

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import  LinkExtractor

import json
import random
import re
from testScrapy.items import MovieItem, CelebrityItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 5,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
#        'FEED_URI': 'file:///D:/123.json',
#        'FEED_FORMAT': 'jsonlines',
#        'FEED_EXPORT_ENCODING': 'utf-8',
        'COOKIES_ENABLED': False,
#        'IMAGES_STORE': '../images/',
        'ITEM_PIPELINES': {
            'testScrapy.pipelines.MovieJsonPipeline': 300,
        }
    }
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/subject/26336252/']
    
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/*', )), callback='parse_movie',  process_links='process_movie_links' ),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        #Rule(LinkExtractor(allow=(r'/celebrity/\d+/', )), callback='parse_celebrity'),
    )
            
    def parse_movie(self, response):
        
        movie_item = MovieItem()
       
        title = response.xpath("//h1/span[@property='v:itemreviewed']/text()").extract_first()
        year = response.css("h1 span.year::text").extract_first()
        mainpic_url = response.css("div.subject a.nbgnbg img::attr(src)").extract()
        
        director_links = response.xpath("//div[@id='info']//a[@rel='v:directedBy']/@href").extract()
        directors = response.xpath("//div[@id='info']//a[@rel='v:directedBy']/text()").extract() 
        
        screenwriter_links = response.xpath("//div[@id='info']").css("span.pl")[1].xpath("./following-sibling::span/a/@href").extract()
        screenwriters = response.xpath("//div[@id='info']").css("span.pl")[1].xpath("./following-sibling::span/a/text()").extract()
        
        actor_links = response.xpath("//div[@id='info']//a[@rel='v:starring']/@href").extract()
        actors = response.xpath("//div[@id='info']//a[@rel='v:starring']/text()").extract()
        
        genre = response.xpath("//div[@id='info']//span[@property='v:genre']/text()").extract()
        
        region = response.xpath("//div[@id='info']").css("span.pl")[4].xpath("./following-sibling::text()").extract_first()
        runtime = response.xpath("//div[@id='info']//span[@property='v:runtime']/@content").extract()
        
        movie_item['title'] = title
        movie_item['year'] = year
        movie_item['directors'] = directors
        movie_item['screenwriters'] = screenwriters
        movie_item['actors'] = actors
        movie_item['genre'] = genre
        movie_item['region'] = region
        movie_item['runtime'] = runtime
        yield movie_item
        
    def parse_celebrity(self, response):
        celebrity_item = CelebrityItem()
        
        name = response.xpath("//div[@id='content']/h1/text()").extract_first()
        pic = response.xpath("//div[@id='headline']").css("div.pic a.nbg img::attr(src)").extract()
         
        gender = response.xpath("//div[@id='headline']").css("div.info").xpath("./ul/li[1]/span[1]/following-sibling::text()").extract()
        constellation = response.xpath("//div[@id='headline']").css("div.info").xpath("./ul/li[2]/span[1]/following-sibling::text()").extract()
        birthdate = response.xpath("//div[@id='headline']").css("div.info").xpath("./ul/li[3]/span[1]/following-sibling::text()").extract()
        birthplace = response.xpath("//div[@id='headline']").css("div.info").xpath("./ul/li[4]/span[1]/following-sibling::text()").extract()
        jobs = response.xpath("//div[@id='headline']").css("div.info").xpath("./ul/li[5]/span[1]/following-sibling::text()").extract()
    
    def process_movie_links(self, links):
        pattern = re.compile(r"/subject/\d+/(.*)")
        for link in links:
            matched = pattern.findall(link.url)
            link.url = link.url.replace(matched[0], '')
        return links
    
    def process_celebrity_links(self, links):
        pass