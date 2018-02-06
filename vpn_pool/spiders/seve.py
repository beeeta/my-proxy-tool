# -*- coding: utf-8 -*-
import scrapy


class SeveSpider(scrapy.Spider):
    name = 'seve'
    allowed_domains = ['proxy.coderbusy.com']
    start_urls = ['https://proxy.coderbusy.com']

    def parse(self, response):
        trs = response.xpath('//tr')[1:]
        items = list()
        for tr in trs:
            ip = tr.xpath('td[1]/text()[2]').extract_first().strip()
            port = tr.xpath('td[2]/text()').extract_first()
            stype = 0 if tr.xpath('td[7]/a/text()').extract_first() == '透明' else 1
            ptype = 'https' if tr.xpath('td[8]/i/text()').extract_first() == 'done' else 'http'
            supost = 1 if tr.xpath('td[9]/i/text()').extract_first() == 'done' else 0
            item = dict(ip=ip,port=port,stype=stype,ptype=ptype,supost=supost)
            items.append(item)
        return items