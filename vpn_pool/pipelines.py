# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from vpn_pool.db import DB
import json


from datetime import datetime

class VpnPoolPipeline(object):

    def open_spider(self,spider):
        nyr = datetime.now().strftime('%Y-%m-%d')
        self.f = open('vpns_by_day_{}.txt'.format(nyr),'w')
        self.db = DB()

    def process_item(self, item, spider):
        self.f.write(str(item))
        self.f.write('\r')
        self.db.add(item)
        return item

    def close_spider(self,spider):
        self.f.close()
        # begin to filter un-active proxy

