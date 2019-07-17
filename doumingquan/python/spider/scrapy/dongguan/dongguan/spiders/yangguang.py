# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dongguan.items import DongguanItem

class YangguangSpider(CrawlSpider):
    name = 'yangguang'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    rules = (
        # 匹配每一个列表页
        Rule(LinkExtractor(allow=r'type=4&page=\d+')),
        # 匹配每一页当中的所有详情页链接
        Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback='parse_item'),
    )

    def parse_item(self, response):
        item = DongguanItem()
        # 获取提问的标题
        title = response.xpath('//div[@class="wzy1"]/table/tr/td[2]/span[1]/text()').extract()
        if title:
            item['title']=title[0]
        else:
            item['title'] = ''
        # 编号
        number = response.xpath('//div[@class="wzy1"]/table/tr/td[2]/span[2]/text()').extract()
        if number:
            item['number'] = number[0]
        else:
            item['number'] = ''

        #反映的内容
        content = response.xpath('//div[@class="wzy1"]//div[@class="contentext"]/text()')
        contents = response.xpath('//div[@class="wzy1"]//td[@class="txt16_3"]/text()')
        if content:
            item['content']=content.extract()[0]
        elif contents:
            item['content'] = contents.extract()[0]
        else:
            item['content'] =''
        # 处理状态
        status =response.xpath('//span[@class="qblue"]/text()')
        status2 = response.xpath('//span[@class="qgrn"]/text()')
        status3 = response.xpath('//span[@class="qred"]/text()')
        if status:
            item['status']=status.extract()[0]
        elif status2:
            item['status'] = status2.extract()[0]
        elif status3:
            item['status'] = status3.extract()[0]
        else:
            item['status']=''
        # url链接
        item['url'] = response.url

        #使用管道保存到数据库中
        yield item
