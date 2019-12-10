# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy_items = response.xpath('//div[@class ="_1ID8B"]//div[@class="_3zucV _2GPIV f-test-vacancy-item i6-sc _3VcZr"]//a/@href').extract()
        for link in vacancy_items:
            yield response.follow(link,self.vacancy_parse)
        #print(vacancy_items)

    def vacancy_parse(self, response:HtmlResponse):
        name = response.xpath('//div[@class="_3MVeX"]//h1/text()').extract_first()
        #salary = response.xpath('//span[@class="_3mfro _2Wp8I ZON4b PlM3e _2JVkc"]/text()').extract()
        salary2 = response.css('div._3MVeX span._2Wp8I span::text').extract()
        print(salary2)
        yield JobparserItem(name=name,salary=salary2,link = response.url, site = 'superjob.ru')




        pass
