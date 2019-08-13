import csv

iter=[
    {'id':2,'name':'wanwu','age':23,'date':20180627},
    {'id':3,'name':'zhaoliu','age':24,'date':20180627},
    {'id':4,'name':'tianqi','age':25,'date':20180627}
]
csv_file=open('zhwy_user_test.csv',encoding="utf-8")    #打开csv文件
# csv_file=open('names.csv',encoding="utf-8")    #打开csv文件

csv_reader_lines = csv.reader(csv_file)   #逐行读取csv文件
date=[]    #创建列表准备接收csv各行数据
renshu = 0

for one_line in csv_reader_lines:
    date.append(one_line)    #将读取的csv分行数据按行存入列表‘date’中
    renshu = renshu + 1    #统计行数
print(date)
#操作字典
# with open('names.csv','w',newline='') as csvf:
#     fieldnames=['id','name','age','date']
#     writer=csv.DictWriter(csvf,fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow({'id':1,'name':'lisii','age':22,'date':20180627})
#     writer.writerows(iter)
# 操作列表
with open('names.csv','w',newline='',encoding="utf-8") as csvf:
    writer =csv.writer(csvf,dialect='excel')
    writer.writerows(date)
    csvf.close()

