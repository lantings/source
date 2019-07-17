# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MeishiItem(scrapy.Item):
    # define the fields for your item here like:

    # 名称：水果沙拉
    name = scrapy.Field()

    # url https://food.hiyd.com/detail-huaxiwangniuroumixian.html
    url = scrapy.Field()

    # 营养素含量（每100克）
    nutrient = scrapy.Field()

    # 热量
    hot_engery = scrapy.Field()

    # 脂肪
    fattiness = scrapy.Field()

    # 碳水化合物
    carbo = scrapy.Field()

    # 蛋白质
    protein = scrapy.Field()

    # 胆固醇
    choles = scrapy.Field()

    # 纤维素
    fibrin = scrapy.Field()

    # 镁
    mg = scrapy.Field()

    # 钙
    ca = scrapy.Field()

    # 铁
    fe = scrapy.Field()

    # 锌
    zn = scrapy.Field()

    # 锰
    mn = scrapy.Field()

    # 铜
    cu = scrapy.Field()

    # 钾
    k = scrapy.Field()

    # 原料
    food = scrapy.Field()

    # # 做法
    method = scrapy.Field()

    # crawl爬虫模板的命令
    # scrapy genspider -t crawl meishi "food.hiyd.com"




