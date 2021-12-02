import scrapy
from amazon_scrapy.items import AmazonScrapyItem
import time
from scrapy.exceptions import CloseSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor



class AmazonSpider(scrapy.Spider):
    name = 'amazon_items'
    allowed_domains = ['amazon.in']

    key_word=input("item name  ")
    start_urls = ["https://www.amazon.in/s?k="+(key_word)]
    
    Rules = (Rule(LinkExtractor(allow=(), restrict_css=('.li.a-last',)), callback="parse", follow= True),)

    def parse(self,response):
        for sel in response.xpath('//*[@class="a-section a-spacing-medium a-text-center"]'):
            time.sleep(5)
            item = AmazonScrapyItem()

            item['brand'] = sel.xpath('.//*[@class="s-line-clamp-1"]//text()').extract_first()
            item['title'] = sel.xpath('.//*[@class="a-size-base-plus a-color-base a-text-normal"]//text()').extract_first()
            item['price'] = sel.css('span.a-price-whole::text').extract_first()
            item['rating'] = sel.css('span.a-icon-alt::text').extract_first()
            item['total_review'] = sel.xpath('.//*[@class="a-row a-size-small"]//a/span/text()').extract_first()
            item['image_url'] = sel.css('img.s-image::attr(src)').extract_first()
            yield item
        next_urls = response.css("li.a-last a::attr(href)").extract()
        for next_url in next_urls:
            if next_url:
                yield scrapy.Request(response.urljoin(next_url), callback=self.parse)
            raise CloseSpider(reason="The end")
