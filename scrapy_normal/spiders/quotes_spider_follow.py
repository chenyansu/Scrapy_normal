import scrapy
from scrapy_redis.spiders import RedisSpider

# class QuotesSpider(RedisSpider):
class QuotesSpider(scrapy.Spider):
    
    redis_key = "quotes_follow:start_urlssc"
    name = "quotes_follow"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ] # [0] 开始网址


    def parse(self,response):
        for quote in response.css('div.quote'):
            yield { # [1] yield语句产出，可以通过-o quotes.json 选项输出
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                # 'tags': quote.css('div.tags a.tag::text').extract(),
            }
        
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
            yield response.follow(next_page, callback=self.parse) # [2] 回调自己，会一直按照分页规则深入地爬下去