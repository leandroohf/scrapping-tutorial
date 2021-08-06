import scrapy

from tutorial.items import QuoteItem
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    #allowed_domains = ['http://quotes.toscrape.com']  # XXX: This make skip the other pages 
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse_author(self, response):
    
        # yield {
        #     'author_name': response.css('.author-title::text').get(),
        #     'author_birthday': response.css('.author-born-date::text').get(),
        #     'author_bornlocation': response.css('.author-born-location::text').get(),
        #     'author_bio': response.css('.author-description::text').get(),
        # }

        quote_item = response.meta['quote_item']

        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')
        
        yield loader.load_item()

    def parse(self, response):
        self.logger.info("========= my first spider ================")
        quotes = response.css("div.quote")

        quote_item = QuoteItem()

        for quote in quotes:

            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css('quote_content', '.text::text')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()

            yield {
                'text': quote.css('.text::text').get(),
                'author': quote.css('.author::text').get(),
                'tags': quote.css(".tag::text").getall(),
            }
            self.logger.debug("-------------------------")
        
            author_url = quote.css('.author + a::attr(href)').get()
            self.logger.info('get author page url')
            #yield response.follow(author_url, callback=self.parse_author)

            # passing the item quote_item from one page to another as metadata
            yield response.follow(author_url, self.parse_author, meta={'quote_item': quote_item})

        # next_page = response.css('li.next a::attr(href)').get()
        # self.logger.debug(f'next_page: {next_page}')

        # if next_page is not None:

        #     self.logger.debug('================ NEXT PAGE ===========')
        #     next_page = response.urljoin(next_page)

        #     self.logger.debug(f'next_page: {next_page}')

        #     yield scrapy.Request(next_page, callback=self.parse)

        for a in response.css('ul.pager a'):

            self.logger.debug('================ NEXT PAGE ===========')
            self.logger.debug(f'a =============> : {a}')
            yield response.follow(a, callback=self.parse)

            self.logger.debug("-------------------------\n\n")