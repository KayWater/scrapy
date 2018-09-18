'''
Created on 2018年9月14日

@author: iw12082
'''

import scrapy
import json
import random
import os

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
        urls = ["http://ip.chinaz.com/getip.aspx"]
        
        with open("../proxy.json") as f:
            for line in f.readlines():
                ip_list = json.loads(line)
                for ip in ip_list["ip_list"]:
                    yield scrapy.Request(url=urls[0], callback=self.parse, meta={"proxy": "http://%s"%ip, "ip":ip}, errback=self.err_parse, dont_filter=True)
            
    def parse(self, response):
        proxy = response.meta["ip"]
        with open("../validProxy.json", "a") as f:
            f.write(proxy+"\n")
            pass
        
    def err_parse(self, failure):
        print(failure.value)
        
    