'''
Created on 2018年9月5日

@author: iw12082
'''
import scrapy
from testScrapy.items import AuthorItem, QuoteItem, TagItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"

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
            tag_item = TagItem()
            tags = quote.css("div.tags a.tag::text").extract()
            text = quote.css("span.text::text").extract_first()
            author = quote.css("small.author::text").extract_first()
            for tag in tags:
                tag_item['name'] = tag
                yield tag_item
            
            author_link = quote.css("small.author + a::attr(href)")

            pass
        
        
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
        