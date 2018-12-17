﻿# -*- coding:utf-8 -*-
'''
                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            佛祖保佑       永无BUG
'''
import os
import csv
import xlrd
import xlwt
import xlsxwriter
import time
import scipy.io as sio
import matplotlib.pyplot as plt
import numpy as np
from ISA_method import ISA_save# 1.从ISA调用ISA_save方法，将分组后的mat转存到excel中
from ISA_weight_method import ISA_group_weight# 2. 分组后评分融合，均值
from ISA_net_method import ISA_group_mid_net# 3.群组均值网络构建
from ISA_inverted_method import ISA_group_inverted # 4. 倒排档，计算用户与均值虚拟用户的Pearson相似度
from ISA_forecase_method import ISA_group_forecast# 5. 计数Pearson相似度等
from ISA_weight_Pearson import	weight_Pearson
from ISA_evaluation_method import ISA_group_evaluation# 6. Top-k推荐并计算nDCG
#from ISA_eva_method import ISA_group_eva# 6. Top-k推荐并计算nDCG

import sys
reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == "__main__":
    t1 = time.time()
    t = [110,111,112,113,114,115,116,117,118,119]
    
    x = 4
	
    k = [[1681,1770,1673,1688,1697,1836,1571,1804,1668,1801],
          [1731,1689,1805,1673,1768,1737,1650,1765,1673,1729],
          [1902,1655,1873,1589,1928,1718,1757,1742,1747,1636]]		  
	
    for i in range(0,5):
        for j in range(3):
			if k[j][i] == 1681:
				continue
			try:
				ISA_group_mid_net(x, t[i], k[j][i])
				ISA_group_inverted(x, t[i], k[j][i])
				weight_Pearson(x, t[i], k[j][i])
				ISA_group_forecast(x, t[i], k[j][i])
				ISA_group_evaluation(x, t[i], k[j][i])
			except:
				ISA_save(x, t[i], k[j][i])
				ISA_group_weight(x, t[i], k[j][i])
				ISA_group_mid_net(x, t[i], k[j][i])
				ISA_group_inverted(x, t[i], k[j][i])
				ISA_group_forecast(x, t[i], k[j][i])
				ISA_group_evaluation(x, t[i], k[j][i])
				continue


    '''
    # 第一步 群组存储到Excel中
    # 第二步 计算群组评分均值
    # 第三步 构建群组均值网络
    # 第四步 倒排档，计算用户与均值虚拟用户的Pearson相似度
    # 第五步 计数Pearson相似度等
    # 第六步 Top-k推荐并计算nDCG
    ISA_save
    ISA_group_ave
    ISA_group_ave_net
    ISA_group_inverted
    Test_split
    ISA_group_forecast
    ISA_group_evaluation

    Test_split(6510)
  
    # 第二步 群组评分预测
    for i in list_isa_242:
        ISA_group_ave(t,i)

    # nmf预测评分与测试集直接对比   效果不好，有效值太少
    for j in list_isa_242:
        #ISA_group_ave_net(t,j)
        #NMF_if_suc(t,j)
        ISA_group_nmf_eva_2(t,j)
    '''
    t2 = time.time()
    print("全部聚类词典划分完成，耗时："+str(t2-t1)+"秒。") #反馈结果
