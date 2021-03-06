from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
from alepe.spiders.TextoProject import TextoProjectSpider

def stop_reactor():
    reactor.stop()

dispatcher.connect(stop_reactor, signal=signals.spider_closed)


text = TextoProjectSpider()
crawler = Crawler(Settings())
crawler.configure()
crawler.crawl(text)
crawler.start()
reactor.run()
