import time
import re
# 1/2/3/4/5周/1月/季度/1年对应时间1天/1
# i=1
#
# classic = time.strftime("%Y%m%d", time.localtime())
# print(classic)
# s = "/opt/datatom/ftpdata/base_test1.txt"
# t = s.split("/")[-1]
#
# s = "opt/tst/dsjzx_test1_201910"
#
# a = r"dsjzx_test"
# a=r"[0,9]{0,8}"
# t = "dsjzx"
# t1="test1"
# res = "%s_%s_([0-9]*)"%(t,t1)
# print(res)
# rest = re.match(res,s)
# # print(re.match(res, s))
# if rest:
#     rest = re.match(res, s).group()
# else:
#     rest=''
# # rest = re.match(res,s).group()
# # print(rest)
#
# st = "/opt/datatom/test/txt_mingquan_table"
# tabe = st.split("/")[-1]
# print(tabe)
# filepath = st.split(tabe)[0]
# print(filepath)
#
# lists = ['/opt/datatom/ftp/base_test1.txt','/opt/datatom/ftp/base_test444.txt','/opt/datatom/ftp/base_test55.txt','/opt/datatom/ftp/base_test222.txt']
# st = '/opt/datatom/ftp/base_test2.txt'
# print(st in lists)

# 表名dsj_test
# 我需要的结果
# txt_dsj_test_20191012
# txt_dsj_test_20191012.txt
# 不需要的是
# txt_dsj_test_20191012_20191022
# txt_dsj_test_20191012_20191022.txt
#
# 一个正则只匹配这2种格式：
# 几个英文字母_表名_8位日期
# 几个英文字母_表名_8位日期.几个英文字母

id = ['txt_mingquan_test_20191112.txt','txt_mingquan_test_qb_20191112.txt','csv_mingquan_test_20191112.txt']
tablename = "mingquan_test"

b = r"(txt|csv)_%s_[0-9]{8}(\.([a-zA-Z]{3}))?"%tablename
# b = r"(txt|csv)_%s_([0-9]{8}|([0-9]{8}\.(.*)))"%mingquan_test

for i in range(len(id)):
    re_match = re.match(b, id[i].split("/")[-1])
    re_match = re.match(b, id[i])
    if(re_match):
        print(re_match.group())






