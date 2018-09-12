'''
Created on 2018年9月12日

@author: iw12082
'''

import scrapy

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 3,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        
        }
    
    def start_requests(self):
        urls = ["https://movie.douban.com/top250"]
        
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        for link in response.css("div.info a::attr(href)"):
            yield response.follow(link, self.parse_movie)
        
        for link in response.css("div.paginator + a::attr(href)"):
            yield response.follow(link, self.parse)
            
    def parse_movie(self, response):
        
        url = response.url 
        
        name = response.xpath("//h1/span[@property='v:itemreviewed']/text()").extract_first()
        year = response.css("h1 span.year::text").extract_first()
        mainpic_url = response.css("div.subject a.nbgnbg img::attr(src)").extract_first()
        
        directors = response.xpath("//div[@id='info']//a[@rel='v:directedBy']/@href").extract()
        
        screenwriters = response.xpath("//div[@id='info']").css("span.pl")[1].xpath("./following-sibling::span/a/@href").extract()
        
        actors = response.xpath("//div[@id='info']//a[@rel='v:starring']/@href").extract()
        
        genre = response.xpath("//div[@id='info']//span[@property='v:genre']/text()").extract()
        
        region = response.xpath("//div[@id='info']").css("span.pl")[4].xpath("./following-sibling::text()").extract_first()
        pass
       