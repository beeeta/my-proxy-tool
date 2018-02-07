# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VpnPoolItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    stype = scrapy.Field()
    ptype = scrapy.Field()
    spost = scrapy.Field()
    dtimen = scrapy.Field()
    isactive = scrapy.Field()
    ctime = scrapy.Field()

if __name__ == '__main__':
    vpn = VpnPoolItem(ip='12.12.12.11',port='42')

