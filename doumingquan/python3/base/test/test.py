
str="/opt/datatom/dana_api/log/shuiwuju_16_88_syrk_logs_info.log"
list = str.split('/')
log = list[5]
table_conf = log[:-4]
print(table_conf)




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