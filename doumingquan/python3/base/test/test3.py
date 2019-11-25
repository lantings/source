

a = {'filename':'1.jpg','file_time':'2019 10-20','16jinzhi':'sfsfs'}
b = {'filename':'2.jpg','file_time':'2019 10-20','16jinzhi':'sfsfs'}
c = {'filename':'3.jpg','file_time':'2019 10-20','16jinzhi':'sfsfs'}
d = {'filename':'4.jpg','file_time':'2019 10-20','16jinzhi':'sfsfs'}
e = {'filename':'5.jpg','file_time':'2019 10-20','16jinzhi':'sfsfs'}
lists=[]
lists.append(a)
lists.append(b)
lists.append(c)
lists.append(d)
lists.append(e)
# print(lists)
# with open("1.txt",'wb') as f:
strs=''
for i in lists:
    strs+= i['filename']+"\u0001"+i['file_time']+"\u0001"+i['16jinzhi']+"\n"
print(strs)


