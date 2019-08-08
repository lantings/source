import configparser  
import sys  
config=configparser.ConfigParser()  
config.add_section("book")  
config.set("book","title","这是标题")  
config.set("book","author","大头爸爸")  
config.add_section("size")  
config.set("size","size",'1024')  
config.write(sys.stdout) 