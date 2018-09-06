'''
Created on 2018年9月5日

@author: iw12082
'''
import scrapy
from _ast import Call
from attr import __author__


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
        for author_link in response.css("small.author + a::attr(href)"):
            yield response.follow(author_link, self.author_parse)
        
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
        def extract_with_css(query):
            return response.css(query).extract_first().strip()
        
        yield {
            "name": extract_with_css("h3.author_title"),
            "birthdate": extract_with_css("span.author-born-date"),
            "bio": extract_with_css("div.author-description"),
            }
        