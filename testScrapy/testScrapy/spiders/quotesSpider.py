'''
Created on 2018年9月5日

@author: iw12082
'''
import scrapy
from testScrapy.items import AuthorItem, QuoteItem
from OpenSSL._util import text

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'testScrapy.pipelines.QuotePipeline': 300,
            },
        'CLOSESPIDER_ITEMCOUNT': 10, #抓取10个条目后停止spider
        'JOBDIR': '../crawls/'+__name__+'-1', #spider 状态保存位置
        }
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
      
    def parse(self, response):
        # follow links to author page
#         for author_link in response.css("small.author + a::attr(href)"):
#             yield response.follow(author_link, self.author_parse)
        
        # extract quote text, author and tags
        for quote in response.css("div.quote"):
            tags = quote.css("div.tags a.tag::text").extract()
            text = quote.css("span.text::text").extract_first()
            author = quote.css("small.author::text").extract_first()
            
            # follow links to auhtor page
            #author_link = quote.css("small.author + a::attr(href)")[0]
            #yield response.follow(author_link, self.author_parse)
            
            quote_item = QuoteItem()
            quote_item['text'] = repr(text)
            quote_item['author'] = author
#            quote_item['tags'] = repr('-'.join(map(str, tag_id)))
            quote_item['tags'] = repr('|'.join(tags))
            yield quote_item
        
        # follow pagination links
        for link in response.css("li.next a::attr(href)"):
            yield response.follow(link, self.parse)
        
#         for quote in response.css("div.quote"):
#             yield {
#                 "text": quote.css("span.text::text").extract_first(),
#                 "author": quote.css("small.author::text").extract_first(),
#                 "tags": quote.css("div.tags a.tag::text").extract()
#             }
#             
#         next_page = response.css("li.next a::attr(href)").extract_first() 
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse)
            
    def author_parse(self, response):
        author_item = AuthorItem()
        
        author_item['name'] = response.css("h3.author-title::text").extract_first()
        author_item['birthdate'] = response.css("span.author-born-date::text").extract_first()
        author_item['birthplace'] = response.css("span.author-born-location::text").extract_first()
        author_item['description'] = response.css("div.author-description::text").extract_first()
        
        yield author_item

    