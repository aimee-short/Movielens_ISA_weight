# -*- coding:utf-8 -*-
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
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def Eva(kk):
    workbook = xlsxwriter.Workbook(r'Movielens_isa_%d_mae_rsme.xlsx'%kk)
    sheet_mae = workbook.add_worksheet('mae')
    for i in range(6):
        sheet_mae.write(0,i, '0.%d'%(i+4))
    sheet_rsme = workbook.add_worksheet('rsme')  # 用户-群组uder_id    item_id   true_rating   forecase_rating  mae  rsme似度
    for i in range(6):
        sheet_rsme.write(0,i, '0.%d'%(i+4))

    def Eva_one(f,t,k,kk):
        t1 = time.time()
        # 测试集向量  f ISA_阙值  ff top_n推荐个数  nn 统计表格第几行/第几个文件   nn
        work_test = xlrd.open_workbook(r'eva_%d/Movielens_isa_%d_%d_weight_forecast.xlsx'%(f,t,k),'rd')
        all_eva = work_test.sheet_by_name('forecast')
        nu = all_eva.nrows# 有title

        sum_mae = 0.0
        sum_rsme = 0.0
        ne = 0
        for i in range(1,nu):
            if all_eva.cell(i,kk+2).ctype == 0 or all_eva.cell(i,kk+2).value == 0:
                continue
            else:
                t_rating = float(all_eva.cell(i,2).value)
                f_rating = float(all_eva.cell(i,kk+2).value)
                chazhi = abs(f_rating - t_rating)/2
                sum_mae += chazhi
                sum_rsme += chazhi ** 2
                ne += 1
        mae = sum_mae/ne
        rsme = math.sqrt(sum_rsme/ne)

        t2 = time.time()
        print("%d_%dmae、rsme评估完成，耗时：" %(t,k) + str(t2 - t1) + "秒。")  # 反馈结果
        return mae,rsme

    t = [110,111,112,113,114,115,116,117,118,119]

    k4 = [[1681,1770,1673,1688,1697,1836,1571,1804,1668,1801],
          [1731,1689,1805,1673,1768,1737,1650,1765,1673,1729],
          [1902,1655,1873,1589,1928,1718,1757,1742,1747,1636]]

    k5 = [[1640,1532,1511,1470,1486,1582,1539,1537,1503,1536],
          [1646,1537,1614,1658,1538,1604,1496,1570,1397,1582],
          [1678,1441,1569,1531,1575,1531,1688,1472,1543,1505]]

    k6 = [[1570,1247,1375,1286,1321,1442,1337,1446,1312,1466],
          [1364,1415,1318,1264,1402,1418,1327,1399,1180,1403],
          [1564,1314,1344,1315,1293,1433,1343,1558,1321,1387]]
    '''
    k72 = [[1338,1153,1114,1104,1122,1156,1215,,1170,1120,1114],
          [    ,1163,1132,1195,1185,1185,1091,1140,,],
          [,,,,,,,,,]]
    '''

    k7 = [[1120,1138,1176,1115,1276,1238,1164,1262,1147,1193],
          [1091,1173,1108,1184,1203,1203,1212,1104,1043,1190],
          [1191,1091,1234,1157,1145,1212,1180,1195,1200,1163]]

    k8 = [[1113,1019,1026,1041,1055,1047,997,1158,1065,1147],
          [1127,1070,1267,1037,1008,1109,1085,1186,1088,1185],
          [1083,1094,1081,1036,1043,1104,1112,1026,1071,1066]]

    k9 = [[970, 935,984,962,937,1053,981,979,1025,911],
          [985, 1018,985,945,971,1049,1008,1011,982,1036],
          [1008, 1038,1040,915,991,982,1023,1047,979,1057]]

    ni = 1
    for i in range(10):
        for j in range(3):
            try:
                mae, rsme = Eva_one(5, t[i], k5[j][i],kk)
                sheet_mae.write(ni, 1, mae)
                sheet_rsme.write(ni, 1, rsme)
            except:
                sheet_mae.write(ni,0,"*")
                sheet_rsme.write(ni,0,"*")
            ni += 1
    ni = 1
    for i in range(10):
        for j in range(3):
            try:
                mae, rsme = Eva_one(6, t[i], k6[j][i],kk)
                sheet_mae.write(ni, 2, mae)
                sheet_rsme.write(ni, 2, rsme)
            except:
                sheet_mae.write(ni,0,"*")
                sheet_rsme.write(ni,0,"*")
            ni += 1
    ni = 1
    for i in range(10):
        for j in range(3):
            try:
                mae, rsme = Eva_one(7, t[i], k7[j][i],kk)
                sheet_mae.write(ni, 3, mae)
                sheet_rsme.write(ni, 3, rsme)
            except:
                sheet_mae.write(ni,0,"*")
                sheet_rsme.write(ni,0,"*")
            ni += 1
    ni = 1
    for i in range(10):
        for j in range(3):
            try:
                mae, rsme = Eva_one(8, t[i], k8[j][i],kk)
                sheet_mae.write(ni, 4, mae)
                sheet_rsme.write(ni, 4, rsme)
            except:
                sheet_mae.write(ni,0,"*")
                sheet_rsme.write(ni,0,"*")
            ni += 1
    ni = 1
    for i in range(10):
        for j in range(3):
            try:
                mae, rsme = Eva_one(9, t[i], k9[j][i],kk)
                sheet_mae.write(ni, 5, mae)
                sheet_rsme.write(ni, 5, rsme)
            except:
                sheet_mae.write(ni,0,"*")
                sheet_rsme.write(ni,0,"*")
            ni += 1
    workbook.close()

if __name__ == "__main__":
    t1 = time.time()
    Eva(30)
    t2 = time.time()
    print("mae、rsme评估全部完成，耗时："+str(t2-t1)+"秒。") #反馈结果
