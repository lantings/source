
str = " this is test "
# strip去掉首尾指定字符
str2 = str.strip()
print(str2)

# find找到返回0，找不到返回-1
str3 = str2.find(' this is test')
print(str3)
info=''
info += "{key}='{value}',".format(key='mingquan', value='123456')
info="{key}='{value}',".format(key='test', value='123456')
print(info)

string = type(info).__name__  #打印出string
# str3 = info.append()
print(string)


