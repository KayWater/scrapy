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
        'ITEM_PIPELINES': {'testScrapy.pipelines.IpJsonPipeline': 300,}   
        }
    
    def start_requests(self):
        start_urls = ["https://www.kuaidaili.com/free/inha/1/"]
        
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
         
        ips = IpsItem()
        ip_addr = response.xpath("//div[@id='list']//td[@data-title='IP']/text()").extract()
        ip_port = response.xpath("//div[@id='list']//td[@data-title='PORT']/text()").extract()
        ip_list = [x+":"+y for x, y in zip(ip_addr, ip_port)]
        for ip in ip_list:  
            yield scrapy.Request('http://www.baidu.com/', meta={"proxy": "http://%s"%ip}, callback=self.test_proxy, errback=self.err_proxy)
        
        ips['ip_list'] = ip_list
        yield ips
        #link = response.xpath("//div[@id='listnav']").css("a.active").xpath("../following-sibling::li[1]/a/@href")
        #link = response.xpath("//div[@id='listnav']//a[@class='active']/../following-sibling::li[1]/a")
        for link in response.xpath("//div[@id='listnav']").css("a.active").xpath("../following-sibling::li[1]/a/@href"):
            yield response.follow(link, self.parse)
    
    def test_proxy(self, response):
        response

    def err_proxy(self, failure):
        failure