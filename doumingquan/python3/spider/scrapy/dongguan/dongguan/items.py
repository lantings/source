# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DongguanItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()

    number = scrapy.Field()

    content = scrapy.Field()

    status = scrapy.Field()

    url = scrapy.Field()

    # crawl爬虫模板的命令
# scrapy genspider -t crawl yangguang "wz.sun0769.com"
