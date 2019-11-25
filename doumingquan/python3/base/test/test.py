
# str="/opt/datatom/dana_api/log/shuiwuju_16_88_syrk_logs_info.log"
# list = str.split('/')
# log = list[5]
# table_conf = log[:-4]
# print(table_conf)
import re
import time
def check_ip(ipAddr):
  compile_ip=re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
  if compile_ip.match(ipAddr):
    return "this is right"
  else:
    return False
str="172.25.16.66"
data = check_ip(str)
print(data)

test = str+"mingquan is very much"
#print(test)
test = "mingquan"
test = test.split(",")[0]
time = "string is sifsff %s"%test
print(test)









# if os.path.exists(table_conf):
#     conf = MyConfigParser()
#     conf.read(table_conf)
#
#     ScheduleType = conf.get('info', 'ScheduleType')
#     # 星环的目标字段
#     TargetList = conf.get('info', 'TargetList')
#     return UnitName, MappingList, SourceTableName, XinghuanAddress, XinghuanUsername, XinghuanPassword, PrimaryKey, HttpfsAddress, XinghuanTableName, XinghuanOrcTableName, Exectimes, AddTimefield, ColumnType, ScheduleType, TargetList
# else:
#     pri.error("params %s is not exists" % table_conf)
#     return 1
# print(conf)