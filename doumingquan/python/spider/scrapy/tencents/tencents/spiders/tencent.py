# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencents.items import TencentItem

class TencentSpider(CrawlSpider):
    name = 'tencent'
    allow_domains = ["hr.tencent.com"]
    start_urls = ['https://hr.tencent.com/position.php?&start=0#']
    pagelink = LinkExtractor(allow=("start=\d+"))
    rules = (
        Rule(pagelink, callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):

            item = TencentItem()
            # 职位名
            item['positionName'] = each.xpath('./td[1]/a/text()').extract()[0]

            # 详情连接
            item['positionLink'] = each.xpath('./td[1]/a/@href').extract()[0]

            # 职位类别(可能会为空)
            text = each.xpath('./td[2]/text()').extract()
            if text:
                item['positionType'] = text[0]
            else:
                item['positionType'] = ''

            # 招聘人数
            item['peopleNum'] = each.xpath('./td[3]/text()').extract()[0]

            # 工作地点
            item['workLocation'] = each.xpath('./td[4]/text()').extract()[0]

            # 发布时间
            item['publishTime'] = each.xpath('./td[5]/text()').extract()[0]

            yield item
