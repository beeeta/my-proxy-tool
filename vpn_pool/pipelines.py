# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from vpn_pool.db import DB
import json

from datetime import datetime
from vpn_pool.utils import check_vpn_validation

class VpnPoolPipeline(object):

    def open_spider(self,spider):
        self.db = DB()

    def process_item(self, item, spider):
        ip = item.get('ip')
        port = item.get('port')
        ex_items = self.db.find_by_ip_port(ip,port)
        if not ex_items:
            self.db.add(item)
        return item

    def close_spider(self,spider):
        check_vpn_validation(self.db)
