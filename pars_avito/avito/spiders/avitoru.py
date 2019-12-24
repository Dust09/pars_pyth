# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader



class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/ufa/avtomobili?cd=1&radius=200']

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath('//a[@class="snippet-link"]/@href').extract()
        for link in ads_links:
            yield response.follow(link,callback=self.parse_ads)

    def parse_ads(self, response:HtmlResponse):
        loader = ItemLoader(item=AvitoItem(), response = response)
        loader.add_xpath('title','//h1[@class = "title-info-title"]/span[@class="title-info-title-text"]/text()')
        loader.add_xpath('photos','//div[@class="gallery-imgs-container js-gallery-imgs-container"]//div[1]/@data-url')
        loader.add_xpath('price','//span[@class="price-value-string js-price-value-string"]//span[@class = "js-item-price"]/text()')
        loader.add_xpath('params','//ul[@class="item-params-list"]//li[@class="item-params-list-item"]/text() | //ul[@class="item-params-list"]//li[@class="item-params-list-item"]/span/text() ')

        yield  loader.load_item()



        #CLASSIC
        #title = response.xpath('//h1[@class = "title-info-title"]/span[@class="title-info-title-text"]/text()').extract_first()
        #photos = response.xpath('//div[@class="gallery-imgs-container js-gallery-imgs-container"]//div[1]/@data-url').extract()
        #print(title,photos)
        #yield AvitoItem(title = title, photos= photos)
        #pass




