import configparser  
import sys  
config=configparser.ConfigParser()  
config.read(u'test.conf',encoding="utf-8-sig")
#print (string.upper(config.get("book","title"))) 
print ("by",config.get("book","title"))
print ("("+config.get("book","time")+")")
 
print (config.get("size","size"))  
 
print (config.sections())  
  
for section in config.sections():  
    print (section)  
    for option in config.options(section):  
        print (" ",option,"=",config.get(section,option)) 