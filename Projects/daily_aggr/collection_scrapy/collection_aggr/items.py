# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

class CollectionAggrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pageurl=Field()
    title=Field()
    type=Field()
    source=Field()
    abstract=Field()
    tags=Field()
    read=Field()
    comment=Field()
    publish_time=Field()
    

