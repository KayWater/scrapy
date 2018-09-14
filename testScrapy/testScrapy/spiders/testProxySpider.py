'''
Created on 2018年9月14日

@author: iw12082
'''

import scrapy
import json
import random

class TestProxySpider(scrapy.Spider):
    name = 'testProxy'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 2,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        'COOKIES_ENABLED': False,
        'DOWNLOAD_MIDDLEWARE': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 100}
    }
    
    def start_requests(self):
        urls = ["http://ip.chinaz.com/linksip"]
        ip_list = self.get_ip()
        for url in urls:
            ip = random.choice(ip_list)
            print(ip)
            yield scrapy.Request(url=url, meta={"proxy": "http://%s"%(ip)}, callback=self.parse)
            
    def parse(self, response):
        
        ip = response.css("dd.fz24::text").extract()
        
    def get_ip(self):
        with open("../proxy.json", 'rb') as f:
            text = f.readline()
            data = json.loads(text)
            return data['ip_list']   