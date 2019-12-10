# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://ufa.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response:HtmlResponse):

        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)   #возвращает стр и будет возвращать до тех пор пока не кончатся страницы

        vacansy_items = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for i in vacansy_items:
            yield response.follow(i, callback=self.vacancy_parse)

    def vacancy_parse(self,response:HtmlResponse):
        name = response.xpath('//h1[@class="header"]//span/text()').extract_first()
        salary = response.xpath('//p[@class="vacancy-salary"]/text()').extract()
        print(name,salary)
        yield JobparserItem(name=name,salary=salary,link = response.url,site = 'hh.ru')










