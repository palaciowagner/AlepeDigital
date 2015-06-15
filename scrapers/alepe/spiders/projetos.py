# -*- coding: utf-8 -*-
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals, Spider, Item, Field
from scrapy.xlib.pydispatch import dispatcher
from scrapy.http import Request
from scrapy.utils.project import get_project_settings
import scrapy
from scrapy.selector import Selector
from alepe.spiders.TextoProjeto import TextoProjetoSpider
from alepe.spiders.CrawlerWorker import CrawlerWorker
from multiprocessing.queues import Queue


#from alepe.items import ProjetoItem


texto_urls = []
class ProjetosSpider(scrapy.Spider):
    name = "projetos"
    allowed_domains = ["alepe.pe.gov.br"]
    start_urls = ["http://www.alepe.pe.gov.br/paginas/?id=3597&catindex=&pagina=1","http://www.alepe.pe.gov.br/paginas/?id=3597&catindex=&pagina=2", ]




    # def setup_crawler(self,spider_name,link):
    #
    #     crawler = Crawler(Settings())
    #
    #     # self.stop_reactor()
    #     crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    #     crawler.configure()
    #     # spider = crawler.spiders.create(spider_name)
    #     spider_name = TextoProjetoSpider(link)
    #
    #     crawler.crawl(spider_name)
    #
    #     crawler.start()
    #     reactor.run()
    #
    #
    #     # texto.start_urls.remove(link)


    def parse(self, response):
        sel = Selector(response)

        projetos = sel.xpath('//table/tr[@class!="titulo"]')

        for projeto in projetos:
            link = str(projeto.xpath('td[1]/a/@href').extract()[0])
            link = link.replace("..","http://www.alepe.pe.gov.br")
            texto_urls.append(link)



            docid = link.split("=")[-1]
            numero = link.split("=")[-2][:-6]

            proposicao = projeto.xpath('td[1]/a/text()').extract()
            autor = projeto.xpath('td[2]/text()').extract()
            situacao = projeto.xpath('td[3]/text()').extract()

            print docid, numero, proposicao[0], autor[0],situacao[0]
            print "DOCID:" + docid+ "\nNUMERO: "+numero+"\nPROPOSICAO: "+proposicao[0]+"\nAUTOR: "+autor[0]+"\nSITUACAO: "+situacao[0]+"\n\n"



texto = TextoProjetoSpider(texto_urls)
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()

crawler.crawl(texto)
crawler.start()

reactor.run()



