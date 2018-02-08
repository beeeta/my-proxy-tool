# -*- coding: utf-8 -*-
import scrapy
import re
from vpn_pool.items import VpnPoolItem
from datetime import datetime

class EveryDaySpider(scrapy.Spider):
    name = 'byday'
    allowed_domains = ['proxy.coderbusy.com']
    start_urls = ['https://proxy.coderbusy.com/article/category/daily-proxy.aspx/']

    def parse(self, response):
        node_hrefs = response.xpath('//a[@class="tile waves-attach waves-effect"]/@href').extract()
        for href in node_hrefs:
            sub_href = response.urljoin(href)
            yield scrapy.Request(sub_href,callback=self.parse_sub)

    def parse_sub(self, response):
        raw_content = response.xpath('//div[@class="card-inner"]/div[2]').extract_first()
        items = raw_content.split('<br>')
        for i in items:
            inf = re.findall(r'(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}):(\d{0,4})@(\w{4,5})#\[(.*)\]',i)
            if inf is not None and len(inf)>0:
                inf = inf[0]
                stype = 1 if inf[3] == '匿名' else 0
                yield dict(ip=inf[0],port=inf[1],ptype=inf[2],stype=stype,isactive=1,ctime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                # vpn = VpnPoolItem(ip=inf[0],port=inf[1],ptype=inf[2],stype=stype,isactive=1,ctime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                # yield vpn
