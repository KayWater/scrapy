'''
Created on 2018年9月13日

@author: iw12082
'''

import scrapy
from testScrapy.items import IpsItem

class ProxySpider(scrapy.Spider):
    name = 'proxy'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 5,
        'USER_AGENT': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        }
    
    def start_requests(self):
        start_urls = ["http://www.xicidaili.com/nn/"]
        
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        
        ips = IpsItem()
        ip_list = response.xpath("//table[@id='ip_list']//tr/td[2]/text()").extract()
        ips['ip_list'] = ip_list
        yield ips