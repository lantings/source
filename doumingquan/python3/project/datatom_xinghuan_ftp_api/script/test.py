#!/usr/bin/python
# -*- coding: UTF-8 -*-
from get_bucket_num import get_file_bucket_num
from xml.sax.handler import ContentHandler
from xml.sax import make_parser




def parseFile(fileName):
	parser = make_parser()
	parser.setContentHandler(ContentHandler())
	parser.parse(fileName)

def analyse_xml(filename):
	parseFile(filename)




if __name__ == '__main__':
	#y=get_file_bucket_num(1024*1024*299.9)
	#print (y)
	filename = '/opt/datatom/dana_ftp_api/script/12345_THJLXXYS_20190716.xml.bak'
	try:
		analyse_xml(filename)
		print(' %s is OK!' % filename)
	except Exception as e:
		print(' Error found in file:%s' % filename)
