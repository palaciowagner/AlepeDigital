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
from alepe.spiders.TextoProject import TextoProjectSpider
from alepe.spiders.CrawlerWorker import CrawlerWorker
from multiprocessing.queues import Queue


#from alepe.items import ProjectItem


text_urls = []
class ProjectsSpider(scrapy.Spider):
    name = "projects"
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
    #     spider_name = TextoProjectSpider(link)
    #
    #     crawler.crawl(spider_name)
    #
    #     crawler.start()
    #     reactor.run()
    #
    #
    #     # text.start_urls.remove(link)


    def parse(self, response):
        sel = Selector(response)

        projects = sel.xpath('//table/tr[@class!="titulo"]')

        for project in projects:
            link = str(project.xpath('td[1]/a/@href').extract()[0])
            link = link.replace("..","http://www.alepe.pe.gov.br")
            text_urls.append(link)



            docid = link.split("=")[-1]
            number = link.split("=")[-2][:-6]

            proposicao = project.xpath('td[1]/a/text()').extract()
            autor = project.xpath('td[2]/text()').extract()
            situacao = project.xpath('td[3]/text()').extract()

            print docid, number, proposicao[0], autor[0],situacao[0]
            print "DOCID:" + docid+ "\nNUMERO: "+number+"\nPROPOSICAO: "+proposicao[0]+"\nAUTOR: "+autor[0]+"\nSITUACAO: "+situacao[0]+"\n\n"



text = TextoProjectSpider(text_urls)
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()

crawler.crawl(text)
crawler.start()

reactor.run()



