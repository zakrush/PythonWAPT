from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from basic_crawler2.items import BasicCrawler2Item
from scrapy.http import Request
import re

class My2Spider(BaseSpider):
    name = 'basic_crawler2'
    allowed_domains = ['packtpub.com']
    start_urls = ['https://packtpub.com']
    
    def parse(self, response):
        hxs = Selector(response)


        visited_links = list()
        links = hxs.xpath('//a/@href').extract()
        link_validator= re.compile(
            "^(?:http|https):\/\/(?:[\w\.\-\+]+:{0,1}[\w\.\-\+]*@)?(?:[a-z0-9\-\.]+)(?::[0-9]+)?(?:\/|\/"
            "(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+)|\?(?:[\w#!:\.\?\+=&amp;%@!\-\/\(\)]+))?$")

        for link in links:
            if link_validator.match(link) and link not in links:
                links.append(link)
                yield Request(link, self.parse)
            else:
                full_link = response.urljoin(link)
                links.append(full_link)
                yield Request(full_link, self.parse)

