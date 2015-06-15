# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher


class DeputadosSpider(scrapy.Spider):
    name = "deputados"
    allowed_domains = ["alepe.pe.gov.br"]
    start_urls = (
        'http://www.alepe.pe.gov.br/',
    )

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//select[@id="porDeputado"]/option')
        for site in sites:
            value = site.xpath('@value').extract()
            desc = site.xpath('text()').extract()

            if (len(value) > 0) and (len(desc) > 0):
                if value[0]:
                    print value[0], desc[0]