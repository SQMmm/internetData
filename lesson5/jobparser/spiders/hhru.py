# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?text=Python&area=113&st=searchVacancy']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header a.bloko-link::attr(href)').extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div.vacancy-title h1.header::text').extract_first()
        salaryFrom = response.xpath(
            "//div[@class='vacancy-title ']/span/span/meta[@itemprop='minValue']//@content").extract_first()
        salaryTo = response.xpath(
            "//div[@class='vacancy-title ']/span/span/meta[@itemprop='maxValue']//@content").extract_first()

        yield JobparserItem(name=name, salaryFrom=salaryFrom, salaryTo=salaryTo, url=response.url,
                            source=self.allowed_domains[0])
