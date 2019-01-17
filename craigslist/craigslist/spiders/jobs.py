# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request

class JobsSpider(scrapy.Spider):
    name = "jobscontent"
    allowed_domains = ["craigslist.org"]
    start_urls = ["https://newyork.craigslist.org/search/egr"]

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

        # scrap next page
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        # call parse_page funtion and pass the metada to the function
        yield Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url, 'Title': title, 'Address':address})


    def parse_page(self, response):
        # parse page with description

        # acces the metada passed
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')

        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract()).strip()
        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type  = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()

        yield{'URL': url, 'Title': title, 'Address':address, 'Description':description, 'Compensation':compensation, 'Employment Type':employment_type}
