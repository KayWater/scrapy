'''
Created on 2018年9月14日

@author: iw12082
'''
import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from testScrapy.spiders import proxySpider, doubanSpider, testProxySpider, zhihuSpider, quotesSpider

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()
#d = runner.crawl(proxySpider.ProxySpider)
#d = runner.crawl(doubanSpider.DoubanSpider)
#d = runner.crawl(testProxySpider.TestProxySpider)
#d = runner.crawl(zhihuSpider.ZhihuSpider)
d = runner.crawl(quotesSpider.QuotesSpider)
#runner.join()
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished