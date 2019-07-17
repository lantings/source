#coding:utf-8
import scrapy
# 导入items文件
from myspider.items import ItcastItem
class ItcastSpider(scrapy.Spider):
	name = "itcast"
	allow_domains = ["http://www.itcast.cn/"]
	start_urls = ['http://www.itcast.cn/channel/teacher.shtml#']

	def parse(self,response):
		# 将所有文本写入到文件当中
		# with open("teacher.html",'wb+') as f:
		# 	f.write(response.body)
		teacher_list = response.xpath("//div[@class='li_txt']")

		teacherItem = []
		for each in teacher_list:
			item = ItcastItem()

			name = each.xpath('./h3/text()').extract()
			title = each.xpath('./h4/text()').extract()
			info = each.xpath('./p/text()').extract()
			# 不能对字符串进行编码，会报错误
			item['name'] = name[0]
			item['title'] = title[0]
			item['info'] = info[0]
			# print(name[0])
			# print(title[0])
			# teacherItem.append(item)

			# 使用yield 将数据放到piplines中(只保存一个老师的数据)
			yield item

			# 直接return不走piplines，使用scrapy crawl itcast -o itcast.json(使用json将数据写入到itcast.json当中)
		# return teacherItem
	
