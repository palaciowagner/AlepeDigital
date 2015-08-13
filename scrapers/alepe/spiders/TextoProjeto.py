# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector


class TextoProjectSpider(scrapy.Spider):

    name = "textproject"
    allowed_domains = ["alepe.pe.gov.br"]
    start_urls = []
    result = None

    def __init__(self, link):
        self.start_urls = link
    def parse(self, response):
        print "aaaaaaaaaa"
        print self.start_urls
        sel = Selector(response)
        self.result = sel.xpath('//div[@id="tituloGeralInternas"/text()]')
        # //*[@id="textConteudo"]/table/tbody/tr/td[1]
        print self.result
