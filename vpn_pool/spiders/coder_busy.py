# -*- coding: utf-8 -*-
import scrapy
import re
from datetime import datetime

class CoderBusySpider(scrapy.Spider):
    name = 'coder'
    allowed_domains = ['proxy.coderbusy.com']
    start_urls = ['https://proxy.coderbusy.com/article/category/daily-proxy.aspx/']

    def parse(self, response):
        yield from self.parse_per_page(response)
        # 获取其他页的数据
        page_url = response.xpath('//a[@class="btn btn-flat waves-attach/@href"]').extract()[-1]
        page_url_index = page_url.split('=')
        if len(page_url_index) == 2 and isinstance(page_url_index[1],int):
            total_page = page_url_index[1]
            for i in range(2,total_page+1):
                relative_page=page_url_index[0]+str(i)
                yield scrapy.Request(response.urljoin(relative_page),callback=self.parse_per_page)

    # 解析页数信息
    def parse_per_page(self,response):
        node_hrefs = response.xpath('//a[@class="tile waves-attach waves-effect"]/@href').extract()
        for href in node_hrefs:
            sub_href = response.urljoin(href)
            yield scrapy.Request(sub_href, callback=self.parse_proxy_content)

    # 解析代理详情页面
    def parse_proxy_content(self, response):
        raw_content = response.xpath('//div[@class="card-inner"]/div[2]').extract_first()
        items = raw_content.split('<br>')
        for i in items:
            inf = re.findall(r'(\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}):(\d{0,4})@(\w{4,5})#\[(.*)\]',i)
            if inf is not None and len(inf)>0:
                inf = inf[0]
                stype = 1 if inf[3] == '匿名' else 0
                yield dict(ip=inf[0],port=inf[1],ptype=inf[2],stype=stype,isactive=1,ctime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))



