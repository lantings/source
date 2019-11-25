#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import paramiko
import logging
import os
import xml.etree.ElementTree as ET
import sys
import ConfigParser
import commands
#from db import OperDb
import datetime
import time
import jaydebeapi
from xml.sax.handler import ContentHandler
from xml.sax import make_parser






reload(sys)  
sys.setdefaultencoding('utf8') 

def parseFile(fileName):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(fileName)
    print("============")

#解析xml文件
def analyse_xml(LocalXmlPath,TxtPath):
	for root, dirs, files in os.walk(LocalXmlPath):
		for i in range(len(files)):
			#status,out = commands.getstatusoutput("cd %s && tail -c 24 %s"%(LocalXmlPath,files[i]))
			xmlFilePath = os.path.abspath("%s/%s"%(LocalXmlPath,files[i]))
			try:
				parseFile(xmlFilePath)
				print(xmlFilePath)
				tree = ET.parse(xmlFilePath)
				root = tree.getroot()
				for child in root:
					each_list = []
					for children in child:
						#print(children.text.replace('\n','').replace('\r',''))
						each_list.append(children.text.replace('\n','').replace('\r','') if children.text else '')
						#print(each_list)
						each_line = '\x01'.join(each_list)
					#print(each_line)
					with open('%s/%s.txt'%(TxtPath,files[i]),'a+') as res:
						res.write(each_line+'\n')
			except Exception as e:
				print("%s 文件不完整！！！"%xmlFilePath)

				

		#os.system("mv %s %s.tmp"%(xmlFilePath,xmlFilePath))
		#os.remove(xmlFilePath)
	

    
if __name__ == '__main__':
	analyse_xml("/opt/datatom/dana_ftp_api/data/huanbaoju/test1","/opt/datatom/dana_ftp_api/data/huanbaoju/test1")
	#parseFile("/opt/datatom/dana_ftp_api/data/huanbaoju/test1/12345_THJLXXYS_20190716.xml.bak")	




