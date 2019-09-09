#coding=utf-8

import os
import logging
from db import OperDb
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_datax_log(logPath,xhTable,sourTable):
    #判断文件是否存在
    keyWord = ["任务启动时刻","任务结束时刻","任务总计耗时","任务平均流量","记录写入速度","读出记录总数","读写失败总数"]
    results = {}
    workflowname = logPath.split('/')[-1].replace('.log','')
    if os.path.exists(logPath):
        with open(logPath,'r') as loger:
            for i in loger.readlines():
                if i.strip().find('任务启动时刻') != -1:
                   results['starttimw'] = i.strip().split(" : ")[1]
                elif i.strip().find('任务结束时刻') != -1:
                    results['endtime'] = i.strip().split(" : ")[1]
                elif i.strip().find('任务总计耗时') != -1:
                    results['time_consuming'] = i.strip().split(" : ")[1].replace(' ','')
                elif i.strip().find('任务平均流量') != -1:
                    results['speed'] = i.strip().split(" : ")[1].replace(' ','')
                elif i.strip().find('记录写入速度') != -1:
                    results['speedlines'] = i.strip().split(" : ")[1].replace(' ','')
                elif i.strip().find('读出记录总数') != -1:
                    results['totallines'] = i.strip().split(" : ")[1].replace(' ','')
                elif i.strip().find('读写失败总数') != -1:
                    results['faillines'] = i.strip().split(" : ")[1].replace(' ','')
        print(results)
        results['xhtable'] = xhTable
        results['sourcetable'] = sourTable
        results['workflowname'] = workflowname
        return results
    else:
        print('The log does not exist!')
        return {}
         
    print(results)

#将数据写入数据表中
def operate_tables(logPath,xhTable,sourTable,tableName):
    dber = OperDb()
    res = check_datax_log(logPath,xhTable,sourTable)
    if res.has_key("starttimw") and res.has_key("faillines"):
        dber.insert_sql(tableName,res)
        return 0
    else:
        logger.error(logPath+"datax Running failure")
        return 1


if __name__ == "__main__":
    operate_tables('/opt/datatom/dana_api/log/RK_JZZ_CARDINFO_json-14_28_25.426.log','rk.RK_JZZ_CARDINFO','sdfd.sdfdsfdg','public.job_run_info')


