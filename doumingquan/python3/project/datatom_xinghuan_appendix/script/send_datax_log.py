#!/usr/bin/python
 
import subprocess
import pipes
import os
 

def sed_log(workname):
	ssh_host = ['172.27.148.54', '172.27.148.55', '172.27.148.56', '172.27.148.57', '172.27.148.58', '172.27.148.59', '172.27.148.60', '172.27.148.61', '172.27.148.62', '172.27.148.63', '172.27.148.64', '172.27.148.65', '172.27.148.66', '172.27.148.72',]
	file_path = '/opt/datatom/dana_api/log/'
 
 	for ip in ssh_host:
 		#print(ip)
 		resp = subprocess.call(['ssh', ip, 'test -e ' + pipes.quote(file_path + workname + '.log')])
		if resp == 0:
			print ("current task execution node is %s"%ip)
			#os.system("rsync -r %s%s.log 172.27.148.53:%s"%(file_path,workname,file_path))
			#os.system("ssh %s \"rm -f %s%s.log\""%(ip,file_path,workname))
			#return ip
		else:
			print ("---------------------")

if __name__ == '__main__':
	currend_node = sed_log('huanbaoju_16_87_test_test1')
	print(currend_node)
