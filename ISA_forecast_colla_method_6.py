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
import sys
reload(sys)
sys.setdefaultencoding('utf8')
def PearsonS(vec1, vec2):
    value = range(len(vec1))

    sum_vec1 = sum([ vec1[i] for i in value])
    sum_vec2 = sum([ vec2[i] for i in value])

    square_sum_vec1 = sum([ pow(vec1[i],2) for i in  value])
    square_sum_vec2 = sum([ pow(vec2[i],2) for i in  value])

    product = sum([ vec1[i]*vec2[i] for i in value])

    numerator = product - (sum_vec1 * sum_vec2 / len(vec1))
    dominator = ((square_sum_vec1 - pow(sum_vec1, 2) / len(vec1)) * (square_sum_vec2 - pow(sum_vec2, 2) / len(vec2))) ** 0.5

    if dominator == 0:
        return 0
    result = numerator / (dominator * 1.0)

    return abs(result)

def ISA_group_mid_Pearson(f,t,k,uid,x):
    #t 训练id    k ISA划分群组数  uid  第几个用户   x 第几个群组
    #测试集
    work_test = xlrd.open_workbook(r'train/Filmtrust_test_split_65%d.xlsx'%(t),'rb')
    t_ov = work_test.sheet_by_name('old_vector')#测试所需对比数据 向量
    t_fk = work_test.sheet_by_name('final_top')#最终top-n比对数据
    t_fkr = workbook.sheet_by_name('final_top_rating')#最终top-n比对数据 评分结果

    # 群组均值网络
    t_group = xlrd.open_workbook(r'sta_%d/Filmtrust_isa_%d_%d_weight.xlsx'%(f,t,k),'rb')#融合后评分 四行 项目dict 计数 均值 方差
    t_ave = t_group.sheet_by_name('weight')

    # 读取群组x的均值向量
    n_item = int(t_dict.cell((x-1)*3,3).value)#  群组x中的项目数量
    list_ave = []
    for i in range(n_item):
        list_ave.append(t_ave.cell(4*(x-1)+2,i+1).value)

    #查找用户u在第gi群组中的位置
    n_user = int(t_dict.cell((x-1)*3,2).value)#用户个数
    list_u = []
    for i in range(n_user):
        if int(t_dict.cell((x-1)*3+1,i).value) == uid:
            u_add = i
            break

    # 读取用户uid的评分向量 从0开始
    for i in range(n_item):
        list_u.append(gr.cell(u_add,i).value)

    # 计算Pearson相似度
    sim = PearsonS(list_u,list_ave)
    return(sim)

def ISA_group_forecast(f,t,k):
    t1 = time.time()

    #是否曾经评过分
    b_rating = xlrd.open_workbook(r'train/Movielens_array_train_%d.xlsx'%t,'rb')
    table = b_rating.sheet_by_index(0)#通过获取
    ncols = table.ncols

    # 每个群组的均值网络
    group_net = xlrd.open_workbook(r'sta_%d/Movielens_isa_%d_%d_weight_net.xlsx'%(f,t,k),'rb')
    g_net = group_net.sheet_by_name('weight_net')# 两边都有title  I_1   G_1
    g_net_all = group_net.sheet_by_name('weight_net_all')# 两边都有title  I_1   G_1

    # 倒排档
    group_inverted = xlrd.open_workbook(r'sta_%d/Movielens_isa_%d_%d_inverted.xlsx'%(f,t,k),'rb')
    g_inv = group_inverted.sheet_by_name('item_ID')

    # 测试集向量
    work_test = xlrd.open_workbook(r'train/Movielens_test_split_%d.xlsx'%(t),'rd')
    t_ov = work_test.sheet_by_name('old_vector')#测试所需对比数据 向量
    t_fk = work_test.sheet_by_name('final')#所有测试项
    nrows = t_fk.nrows
    n_u = t_ov.nrows-1# 测试用户数量 因为首行为空，所以使用时应该减一

    # 创建预测评分矩阵
    workbook = xlsxwriter.Workbook(r'colla_k/eva_%d/Movielens_isa_%d_%d_weight_forecast.xlsx'%(f,t,k))
    sheet_P = workbook.add_worksheet('Pearson')#用户-群组Pearson相似度
    sheet_f = workbook.add_worksheet('forecast')
    sheet_k = workbook.add_worksheet('top-gid')
    sheet_s = workbook.add_worksheet('top-p')
    sheet_r = workbook.add_worksheet('top-rating')

    sheet_f.write(0,0,'user_id')
    sheet_f.write(0,1,'item_id')
    sheet_f.write(0,2,'true_rating')
    for i in range(10):
        sheet_f.write(0,i+3,i+1)

    sheet_k.write(0, 0, 'user_id')
    sheet_k.write(0, 1, 'item_id')
    sheet_k.write(0, 2, 'true_rating')
    sheet_k.write(0, 3, 'Count_effec')
    sheet_k.write(0, 4, 'Sorted_gid')
    sheet_s.write(0, 0, 'user_id')
    sheet_s.write(0, 1, 'item_id')
    sheet_s.write(0, 2, 'true_rating')
    sheet_s.write(0, 3, 'Count_effec')
    sheet_s.write(0, 4, 'Sorted_pearson')
    sheet_r.write(0, 0, 'user_id')
    sheet_r.write(0, 1, 'item_id')
    sheet_r.write(0, 2, 'true_rating')
    sheet_r.write(0, 3, 'Count_effec')
    sheet_r.write(0, 4, 'Sorted_rating')
    for i in range(n_u):# 写入user id
        sheet_P.write(i,0,t_ov.cell(i,0).value)
    for i in range(k):# 从0开始 项目id写入
        sheet_P.write(0,i+1,'G_%d'%(i+1))

    # 分别读取user vector跟 group vector
    list_g = [[] for j in range(ncols)]
    list_u = [[] for j in range(ncols)]
    for i in range(k):
        for j in range(ncols):
            list_g[i].append(float(g_net.cell(i+1,j+1).value))

    for i in range(n_u):
        for j in range(ncols):
            try:
                list_u[i].append(int(t_ov.cell(i+1,j+1).value))#用user id 有item抬头 空了一行
            except:
                break
    # 计算Pearson相似度
    list_P = [[] for i in range(k)]
    for i in range(n_u):
        for j in range(k):
            try:
                p = PearsonS(list_u[i],list_g[j])
            except:
                p = 0
            sheet_P.write(i+1,j+1,p)
            list_P[i].append(p)
    mae = 0
    rsme = 0
    now_uid = int(t_fk.cell(0,0).value)
    dict_u = {}
    ni = 0#第几个用户
    for i in range(nrows):#第i条记录
        uid = int(t_fk.cell(i,0).value)
        iid = int(t_fk.cell(i,1).value)
        sheet_f.write(i+1, 0, uid)
        sheet_f.write(i+1, 1, iid)
        sheet_f.write(i+1, 2, t_fk.cell(i,2).value)
        sheet_k.write(i + 1, 0, uid)
        sheet_k.write(i + 1, 1, iid)
        sheet_k.write(i + 1, 2, t_fk.cell(i, 2).value)
        sheet_s.write(i + 1, 0, uid)
        sheet_s.write(i + 1, 1, iid)
        sheet_s.write(i + 1, 2, t_fk.cell(i, 2).value)
        sheet_r.write(i + 1, 0, uid)
        sheet_r.write(i + 1, 1, iid)
        sheet_r.write(i + 1, 2, t_fk.cell(i, 2).value)
        ng = int(g_inv.cell(iid,1).value)#每个item所属群组数  有title
        list_id = []
        list_r = []
        sum_p = []
        all_p = 0.0
        if ng > 0:
            for ii in range(ng):#遍历item所在的每个群组   item + group  未必包含user
                gid = int(g_inv.cell(iid,ii+2).value)#群组id
                if g_net_all.cell(gid,iid).ctype == 0 or g_net_all.cell(gid,iid).value == 0:#有些群组中虽然包含user跟item，但其实并没有评分内容，需要判断  有title
                    continue
                else:
                    list_id.append(gid)
                    sum_p.append(float(list_P[ni][gid-1]))
                    r_w = float(g_net_all.cell(gid,iid).value)
                    list_r.append(r_w)#群组Virtual user基于专业度的加权值
        if len(list_id) > 0:
            top_p = sorted(enumerate(sum_p), key=lambda x: x[1],reverse=True)
            sheet_k.write(i + 1, 3, len(list_id))
            sheet_s.write(i + 1, 3, len(list_id))
            sheet_r.write(i + 1, 3, len(list_id))
            list_ep = []
            for iid1 in range(len(list_id)):
                ads = top_p[iid1][0]
                sheet_k.write(i + 1,iid1+4,list_id[ads])
                sheet_s.write(i + 1, iid1 + 4, top_p[iid1][1])
                sheet_r.write(i + 1, iid1 + 4, list_r[iid1])
                list_ep.append(top_p[iid1][1])
                all_p += top_p[iid1][1]
                sum_result = 0.0
                if all_p != 0:
                    list_one = map(lambda x: x / all_p, list_ep)
                    for id2 in range(len(list_ep)):
                        sum_result += list_one[id2]*list_r[id2]
                    sheet_f.write(i+1,iid1+3,sum_result)

    workbook.close()
    t2 = time.time()
    print("%d预测值计算完成，耗时："%k+str(t2-t1)+"秒。") #反馈结果

if __name__ == "__main__":
    t1 = time.time()
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

    for i in range(10):
        for j in range(3):
            ISA_group_forecast(6, t[i], k6[j][i])
    for i in range(10):
        for j in range(3):
            ISA_group_forecast(7, t[i], k7[j][i])
    t2 = time.time()
    print("预测值、MAE、RSME计算完成，耗时：" + str(t2 - t1) + "秒。")  # 反馈结果