# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem

class TencentpositionSpider(scrapy.Spider):
    name = 'tencent'

    allowed_domains = ['tencent.com']

    # 腾讯社招url
    url = "http://hr.tencent.com/position.php?&start="

    offset = 0

    start_urls = [url+str(offset)]

    def parse(self, response):
        for each in response.xpath("//tr[@class='even'] | //tr[@class='odd']"):
            item = TencentItem()
            # 职位名
            item['positionName'] = each.xpath('./td[1]/a/text()').extract()[0]

            # 详情连接
            item['positionLink'] = each.xpath('./td[1]/a/@href').extract()[0]

            # 职位类别(可能会为空)
            text = each.xpath('./td[2]/text()').extract()
            if text:
                item['positionType'] =text[0]
            else:
                item['positionType'] =''

            # 招聘人数
            item['peopleNum'] = each.xpath('./td[3]/text()').extract()[0]

            # 工作地点
            item['workLocation'] = each.xpath('./td[4]/text()').extract()[0]

            # 发布时间
            item['publishTime'] = each.xpath('./td[5]/text()').extract()[0]

            yield item

        # 一共302页
        if self.offset < 3020:
        # 偏移量每次加10
            self.offset += 10

        # 拼接url,回调进行重新请求
        yield scrapy.Request(self.url + str(self.offset), callback=self.parse)


