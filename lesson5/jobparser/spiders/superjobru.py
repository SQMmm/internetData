# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.icMQ_ _1_Cht _3ze9n.f-test-button-dalshe.f-test-link-dalshe::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)
        vacancy = response.xpath("//div[@class='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/../@href").extract()
        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1._3mfro.rFbjy.s1nFK._2JVkc::text').extract_first()
        salaryFrom = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span[1]/text()").extract_first()
        salaryTo = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']/span[3]/text()").extract_first()

        yield JobparserItem(name=name, salaryFrom=salaryFrom, salaryTo=salaryTo, url=response.url,
                            source=self.allowed_domains[0])
