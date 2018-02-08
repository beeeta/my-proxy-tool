# -*- coding: utf-8 -*-
import scrapy
from vpn_pool.items import  VpnPoolItem

from datetime import datetime

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
            spost = 1 if tr.xpath('td[9]/i/text()').extract_first() == 'done' else 0
            dtimen = tr.xpath('td[10]/text()').extract_first().split(' ')[0]
            isactive = 1
            ctime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            vpn = VpnPoolItem(ip=ip,port=port,stype=stype,ptype=ptype,spost=spost,dtimen=dtimen,isactive=isactive,ctime=ctime)
            items.append(vpn)
        yield  items
        # 下一页
        print('------------------- spider seve finished ------------------------')