# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://newyork.craigslist.org/search/egr/']

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')

        # extract titles, addres n urls
        for job in jobs:

            title = job.xpath('a/text()').extract_first()

            # extract_first("") which means if there is no result, the result is “”.
            # [2:-1] removes the parenthesis
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]

            relative_url = job.xpath('a/@href').extract_first()

            absolute_url = response.urljoin(relative_url)

            yield{'URL':absolute_url, 'Title':title, 'Address':address}
