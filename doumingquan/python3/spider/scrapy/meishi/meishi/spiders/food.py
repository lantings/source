# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from meishi.items import MeishiItem

class FoodSpider(CrawlSpider):
    name = 'food'
    allowed_domains = ['food.hiyd.com']
    start_urls = ['https://food.hiyd.com/list-132-html?page=1']

    rules = (
        # 匹配列表页 list-132-html?page=
        Rule(LinkExtractor(allow=r'list-132-html\?page=\d+')),
        # 匹配详情页
        Rule(LinkExtractor(allow=r'/detail-\w+.html'), callback='parse_item'),
    )

    def parse_item(self, response):

        item = MeishiItem()

        # 名称：水果沙拉
        name = response.xpath('//div[@class="info-base"]/div/div/img/@alt').extract()
        item['name'] = name[0]

        # url https://food.hiyd.com/detail-huaxiwangniuroumixian.html
        url = response.url
        item['url'] = url

        # 营养素含量（每100克）
        nutrient = response.xpath('//div[@id="nutr-info"]/ul/li[1]/em/text()').extract()
        item['nutrient'] = nutrient[0]

        # 热量
        hot_engery = response.xpath('//div[@id="nutr-info"]/ul/li[2]/em/text()').extract()
        item['hot_engery'] = hot_engery[0]

        # 脂肪
        fattiness = response.xpath('//div[@id="nutr-info"]/ul/li[3]/em/text()').extract()
        item['fattiness'] = fattiness[0]

        # 碳水化合物
        carbo = response.xpath('//div[@id="nutr-info"]/ul/li[4]/em/text()').extract()
        item['carbo'] = carbo[0]

        # 蛋白质
        protein = response.xpath('//div[@id="nutr-info"]/ul/li[5]/em/text()').extract()
        item['protein'] = protein[0]

        # 胆固醇
        choles = response.xpath('//div[@id="nutr-info"]/ul/li[6]/em/text()').extract()
        item['choles'] = choles[0]

        # 纤维素
        fibrin = response.xpath('//div[@id="nutr-info"]/ul/li[8]/em/text()').extract()
        item['fibrin'] = fibrin[0]

        # 镁
        mg = response.xpath('//ul[@class="no-margin"]/li[2]/em/text()').extract()
        item['mg'] = mg[0]

        # 钙
        ca = response.xpath('//ul[@class="no-margin"]/li[3]/em/text()').extract()
        item['ca'] = ca[0]

        # 铁
        fe = response.xpath('//ul[@class="no-margin"]/li[4]/em/text()').extract()
        item['fe'] = fe[0]

        # 锌
        zn = response.xpath('//ul[@class="no-margin"]/li[5]/em/text()').extract()
        item['zn'] = zn[0]

        # 锰
        mn = response.xpath('//ul[@class="no-margin"]/li[7]/em/text()').extract()
        item['mn'] = mn[0]

        # 铜
        cu = response.xpath('//ul[@class="no-margin"]/li[6]/em/text()').extract()
        item['cu'] = cu[0]

        # 钾
        k = response.xpath('//ul[@class="no-margin"]/li[8]/em/text()').extract()
        item['k'] = k[0]

        # 原料
        food = response.xpath('//div[@class="info-need"]/div[@class="box-bd"]/ul/li/a/span/text()').extract()
        str = ''.join(i for i in food)
        # print(str)
        tmp = str.replace('\n', '').replace(' ', '').replace('\u3000', '').replace('\r', '')
        item['food'] = tmp


        # 做法
        method = response.xpath('//div[@class="info-need"]/div[@class="box-bd"]/div[@class="intro"]/text()').extract()
        tmpe = ''.join(i for i in method)
        # tmpe = ''.join(method)
        # print(tmpe)
        tmps = tmpe.replace('\n', '').replace(' ', '').replace('\u3000', '').replace('\r', '')
        item['method'] = tmps

        return item
