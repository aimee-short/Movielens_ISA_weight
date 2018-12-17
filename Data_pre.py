#-*- coding: utf-8 -*-
import sys
import math
import xlrd
import xlwt
import xlsxwriter
import random
import time
import os
from operator import itemgetter

#相似度到底是怎么计算出出来的

def loadfile(filename):#载入文件
    ''' load a file, return a generator. 载入文件，返回一个【生成器】'''
    fp = open(filename, 'r')
    for i, line in enumerate(fp):
        yield line.strip('\r\n')#读取整个文本内容，换行分隔，存储每一行内容
        '''
        简单地讲，yield 的作用就是把一个函数变成一个 generator，带有 yield 的函数不再是一个普通函数，Python 解释器会将其视为一个 generator，调用 fab(5) 不会执行 fab 函数，而是返回一个 iterable 对象！在 for 循环执行时，每次循环都会执行 fab 函数内部的代码，执行到 yield b 时，fab 函数就返回一个迭代值，下次迭代时，代码从 yield b 的下一条语句继续执行，而函数的本地变量看起来和上次中断执行前是完全一样的，于是函数继续执行，直到再次遇到 yield。
        https://www.ibm.com/developerworks/cn/opensource/os-cn-python-yield/
        为了降低对内存的占用
        yield内存占用始终为常数
        '''
    fp.close()
def generate_dataset(t):#70%训练集
    ''' load rating data and split it to training set and test set 载入并分割训练集测试集'''
    filename = os.path.join('ml-100k', 'u.data')#读取文件
    pivot=0.8
    random.seed(t)
    # 1. 创建一个Excel文件
    workbook = xlsxwriter.Workbook(r'train\\Movielens_array_train_11%d.xlsx'%t)
    # 2. 创建一个工作表sheet对象
    sheet1 = workbook.add_worksheet('train')
    f_test = open(r'train\\Movielens_ratings_test_11%d.txt'%t,'w')

    for line in loadfile(filename):#逐行读取载入文件中
        print(line)
        user, movie, rating, _ = line.split()#分割  读取用户，电影，评分信息
        # split the data by pivot
        if random.random() < pivot:#中心，枢轴
            sheet1.write(int(user)-1,int(movie)-1,float(rating)*2)
        else:
            f_test.write("%d %d %d\n"%(int(user),int(movie),float(rating)*2))
    f_test.close()
    workbook.close()

if __name__ == "__main__":
    for i in range(2,11):
        generate_dataset(i)