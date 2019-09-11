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

        #CODE for scrapping_emails
        emails = hxs.xpath("//*[contains(text(),'@')]").extract()
        for email in emails:
            mail = BasicCrawler2Item()
            mail['email'] = email
            mail['location_url'] = response.url
            yield mail

        #CODE for FORMS
        forms = hxs.xpath("//form/@action").extract()
        for form in forms:
            formy = BasicCrawler2Item()
            formy['forme'] = form
            formy['location_url'] = response.url
            yield formy

        #CODE for comments
        comments = hxs.xpath('//comment()').extract()

        for comment in comments:
            comm = BasicCrawler2Item()
            comm['comment'] = comment
            comm['location_url'] = response.url
            yield comm

        #for recursive links
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

