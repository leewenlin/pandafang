# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PandafangItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #pass
    dong = scrapy.Field()
    unit = scrapy.Field()
    layer = scrapy.Field()
    fang = scrapy.Field()
    name=scrapy.Field()
    area =scrapy.Field()
    price = scrapy.Field()
    url = scrapy.Field()
    furl = scrapy.Field()
    fn=scrapy.Field()
    

    