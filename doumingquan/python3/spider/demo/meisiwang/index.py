import urllib.request
from lxml import etree

url = "https://www.meishij.net/china-food/"
response = urllib.request.Request(url)
html = urllib.request.urlopen(response).read()
# print(html)
content = etree.HTML(html)
# print(content)

# 返回所有匹配成功的列表集合
food_name = content.xpath('//div[@class="listtyle1"]/a/@title')
picture = content.xpath('//div[@class="listtyle1"]/a/img/@src')
food_name = content.xpath('//div[@class="c1"]/strong/text()')
hot_comment = content.xpath('//div[@class="c1"]/span/text()')
writer	 = content.xpath('//div[@class="c1"]/em/text()')
step =   content.xpath('//li[@class="li1"]/text()')
style =  content.xpath('//li[@class="li2"]/text()')
# print(food_name)
# print(writer)
# print(hot_comment)
# print(picture)
# print(step)
# print(style)

food_list = content.xpath('//div[@class="listtyle1"]')
for link in food_list:
	print(link)
# picture = food_list.xpath('/a/img/@src')
# print(food_list)





	
