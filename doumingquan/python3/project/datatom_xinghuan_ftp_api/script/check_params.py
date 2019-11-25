#coding=utf-8


import re
import json

Tres = {}
result = []
def check_params(UnitId, SourceTableName, XinghuanTableName, XinghuanOrcTableName, MappingList, Exectimes, WorkflowTime, ColumnType):
    #校验委办局id，标准全是数字
    res = re.match(r'^[0-9]{1,}$',UnitId)
    check_type('UnitId', UnitId, 'str', res)


    #检测传过来的表的格式标注格式owner.tablename
    res = re.match(r'^[a-zA-Z0-9_]{1,}\.{1}[a-zA-Z0-9_]{1,}$', SourceTableName)
    check_type('SourceTableName', SourceTableName, 'str', res)

    res = re.match(r'^[a-zA-Z0-9_]{1,}\.{1}[a-zA-Z0-9_]{1,}$', XinghuanTableName)
    check_type('SourceTableName', SourceTableName, 'str', res)

    res = re.match(r'^[a-zA-Z0-9_]{1,}\.{1}[a-zA-Z0-9_]{1,}$', XinghuanOrcTableName)
    check_type('SourceTableName', SourceTableName, 'str', res)

    #检验字段：规则list
    check_type('MappingList', MappingList, 'list', 'res')

    # #检验主键
    # res = re.match(r"^([0-9]{1,3}\.){3}[0-9]{1,3}$", ip)

    #检测执行次数-1，正整数
    res = re.match(r'^[\-|0-9][0-9]{1,}$', Exectimes)
    check_type('Exectimes', Exectimes, 'list', res)

    #检测增量全量2表示全量，其他表示增量
    check_type('Execrate',Execrate,'list',res)

    #检测时间调度：dict
    check_type('WorkflowTime', WorkflowTime, 'dict', 'res')

    #检测业务时间类型date，varchar,timestamp,empty
    res = re.match(r'^(date|varchar|empty|timestamp)$', ColumnType)
    check_type('ColumnType', ColumnType, 'str', res)


    check_type('TargetList', TargetList, 'list', 'res')
    print(result)



def check_type(columnName, column, columnType, res):
    tmp = {}
    ty = type(column).__name__
    if ty != columnType:
        resStr = "%s should be %s"%(columnName,columnType)
        tmp['type'] = resStr
    if res is None:
        tmp['value'] = "The parameter [%s] value is incorrect. Please check it"%(columnName)
    result.append(tmp)


        

def check_para_num(params, keysList):
    lostColumns = []
    for i in keysList:
        if not params.has_key(i):
            lostColumns.append(i)
    if len(lostColumns) > 0:
        res = {
            "code":10003,
            "result":{
                "error":"缺失以下参数，请检查传入参数",
                "lostColumns": lostColumns
            }
        }
        return lostColumns,res
    else:
        return lostColumns,{}

if __name__ == '__main__':
    check_params('bowen','bowen','bowen','bowen','bowen','bowen','bowen','bowen')
