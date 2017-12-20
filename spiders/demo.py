# -*- coding: utf-8 -*-
import scrapy
from zimuku.items import ZimukuItem
import sys
reload(sys)                     #这句不能少！！！
sys.setdefaultencoding('utf-8')

class DemoSpider(scrapy.Spider):
    name = "demo"
    allowed_domains = ["zimuku.net"]
    start_urls = ['http://zimuku.net/']

    def parse(self, response):
    	item={}
        names=response.xpath('//b/text()').extract()
        num=0
        for name in names:      #不能用while！！！当list[x]为空或dict['xxx']为空就出错
            item[str(num)]=str(name)
            num+=1
        item['num']=num
        yield item
        nextpage=response.xpath('//a[@class="next"]/@href').extract()[0]
        if str(nextpage):
        	url='http://zimuku.net'+str(nextpage)
        	yield scrapy.Request(url,callback=self.parse)