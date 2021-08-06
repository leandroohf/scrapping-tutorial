import scrapy
from scrapy.http import FormRequest

# from tutorial.items import QuoteItem
# from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = 'quotes-login'

    #allowed_domains = ['http://quotes.toscrape.com']  # XXX: This make skip the other pages 
    start_urls = ['http://quotes.toscrape.com/login']

    def start_scrap(self,response):

        if response.status != 200:
            
            self.logger.error("Login failed!")
            
            return 

        self.logger.info('========== Start scrapping =========== ')
        quotes = response.css("div.quote")

        #quote_item = QuoteItem()

        for quote in quotes:

            text = quote.css('.text::text').get()
            author = quote.css('.author::text').get()
            tags = quote.css(".tag::text").getall()

            self.logger.info(f'text: {text}')
            self.logger.info(f'author: {author}')
            self.logger.info(f'tags: {tags}')

            self.logger.debug("-------------------------")

    def parse(self, response):
    
        token = response.css('form input::attr(value)').get()
        
        self.logger.info(f"token: {token}")

        return FormRequest.from_response(response,formdata={
            'csrf_token': token, 
            'username': 'leandro@gmail.com',
            'password': 'dadisgood'
        }, callback=self.start_scrap)