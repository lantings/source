#!/usr/bin/python
# -*- coding: UTF-8 -*-
import math


def get_num(mb):
	num = int(mb)
	for  i in range(2,num):
		if num % i == 0 :
			return False
		else:
			continue
	if i == num - 1:
		return True

def get_file_bucket_num(bit):
	mb = math.ceil(float(bit)/104857600)
	if mb > 3:
		while True:
			if get_num(mb):
				return int(mb)
				break
			mb += 1
	else:
		mb = 3
		return int(mb)

if __name__ == '__main__':
	x = get_file_bucket_num(1233423123)
	print(x)


