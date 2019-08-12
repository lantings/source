# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanmovie'
    allowed_domains = ['douban.com']
    url = 'https://movie.douban.com/top250?start='
    offset = 0
    start_urls =(
        url + str(offset),
    )

    def parse(self, response):
        item =  DoubanItem()
        # 整个信息都在这个info中
        info = response.xpath('//div[@class="info"]')

        for each in info:
            # 电影名称
            title = each.xpath('.//span[@class="title"][1]/text()').extract()
            item['title'] = title[0]

            # 电影信息
            info = each.xpath('.//div[@class="bd"]/p/text()').extract()
            item['info'] = info[0]

            # 电影评分
            rate = each.xpath('.//span[@class="rating_num"][1]/text()').extract()
            item['rate'] = rate[0]
            # 电影简介
            introduce = each.xpath('.//p[@class="quote"]/text()').extract()
            if introduce:
                item['introduce'] = introduce[0]

            yield item

        if self.offset<225:
            self.offset+=25
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)





