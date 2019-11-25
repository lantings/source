#!/usr/bin/env python
#encoding: utf-8
import binascii
fh = open("F:\phpStudy\WWW\git\source\doumingquan\python3\/base\/test\/1.jpg", 'rb')
a = fh.read()
#print 'raw: ',`a`,type(a)
hexstr = binascii.b2a_hex(a)
print (a)
print (hexstr)
str = binascii.a2b_hex(hexstr)
if(str==a):
    print(True)
else:
    print(False)
list = []
hexstr=binascii.hexlify(a)
list.append(hexstr)
print(hexstr)
hexstr=binascii.unhexlify(hexstr)
print(hexstr)
f = open("F:\phpStudy\WWW\git\source\doumingquan\python3\/base\/test\/2.jpg", 'wb')
f.write(hexstr)



