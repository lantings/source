# coding: UTF-8
"""
python2
operate xml
"""

import os
import sys
import time
import xml.etree.ElementTree as ET

# reload(sys)
# sys.setdefaultencoding('utf8')


class OpreateXml():
    """operate xml"""
    #获取文件的根目录
    def test(self,filename):
        xmlFilePath = os.path.abspath("12345.xml")
        print(xmlFilePath)
        # try:
        tree = ET.parse(xmlFilePath)

        print ("tree type:", type(tree))

        # 获得根节点
        root = tree.getroot()
        print(root)

        for neighbor in root.iter('neighbor'):
            print (neighbor.attrib)
        # except Exception as e:  # 捕获除与程序退出sys.exit()相关之外的所有异常
        #     print ("parse test.xml fail!")
        #     sys.exit()
        for child in root:
            #print(child.tag, ":-------------------------", )
            #print(len(child))
            #if len(child) != 18:
            each_list = []
            for children in child:
                print(children.text)
                each_list.append(children.text.strip() if children.text else '')
                each_line = '\x01'.join(each_list)
            #print(each_line)
            with open('12345.txt','a+') as res:
                res.write(each_line+'\n')
        #os.system("sed -i '/^$/d' E:\\wbwworks\\xml\\sendwpinfo1.txt")



if __name__ == "__main__":
    start_time = time.time()
    print(start_time)
    oxml = OpreateXml()
    oxml.test("12345.xml")
    end_time = time.time()
    use_time = end_time - start_time
    print(use_time)