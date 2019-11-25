# coding=utf-8

'''
1-将图片转化为数组并存为二进制文件
2-从二进制文件中读取数并重新恢复为图片
'''

from __future__ import print_function
import numpy
import PIL.Image
import pickle
import matplotlib.pyplot
import pdb


class Operation(object):
    image_base_path = "../image/"
    data_base_path = "../data/"

    def image_to_array(self, filenames):
        """
        将图片转化为数组并存为二进制文件
        """
        n = filenames.__len__()  # 获取图片个数
        print("图片的个数是:",n)
        result = numpy.array([])  # 创建一个空的一维数组
        print("开始将图片转化为数组")
        for i in range(n):
            image = PIL.Image.open(self.image_base_path + filenames[i])
            print(image.split())
            r, g, b = image.split()  # rgb通道分离
            # 注意：下面一定要reshpae(1024)使其变为一维数组，否则拼接的数据会出现错误，导致无法恢复图片
            print('this is r',numpy.array(r))
            r_arr = numpy.array(r).reshape((300,2))
            g_arr = numpy.array(g).reshape((512,2))
            b_arr = numpy.array(b).reshape((512,2))
            # 行拼接，类似于接火车；最终结果：共n行，一行3072列，为一张图片的rgb值
            image_arr = numpy.concatenate((r_arr, g_arr, b_arr))
            result = numpy.concatenate((result, image_arr))

        result = result.reshape(n, 3072)  # 将一维数组转化为n行3072列的二维数组
        print("转化数组over，开始保存为文件")
        file_path = self.data_base_path + 'data2.bin'
        with open(file_path, mode='wb') as f:
            pickle.dump(result, f)
        print("保存成功")

    def array_to_image(self, filename):
        '''
        从二进制文件中读取数据并重新恢复为图片
        '''
        with open(self.data_base_path + filename, mode='rb') as f:
            arr = pickle.load(f)  # 加载并反序列化数据
        rows = arr.shape[0]  # rows=5
        # pdb.set_trace()
        # print("rows:",rows)
        arr = arr.reshape(rows, 3, 32, 32)
        print(arr)  # 打印数组
        for index in range(rows):
            a = arr[index]
            # 得到RGB通道
            r = PIL.Image.fromarray(a[0]).convert('L')
            g = PIL.Image.fromarray(a[1]).convert('L')
            b = PIL.Image.fromarray(a[2]).convert('L')
            image = PIL.Image.merge("RGB", (r, g, b))
            # 显示图片
            matplotlib.pyplot.imshow(image)
            matplotlib.pyplot.show()
            # image.save(self.image_base_path + "result" + str(index) + ".png",'png')


if __name__ == "__main__":
    my_operator = Operation()
    images = []
    for j in range(3):
        images.append(str(j) + ".jpg")
    print(images)
    my_operator.image_to_array(images)
    # my_operator.array_to_image('data2.bin')

# 原文链接：https: // blog.csdn.net / qq_27170195 / article / details / 78192756