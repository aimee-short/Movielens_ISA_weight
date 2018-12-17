# Movielens_ISA_weight
----------------------------------------数据预处理--------------------
Step1：	
	目的：划分训练集测试集（Success）
	注意：excel无抬头 评分*2（0~10）
	工具：Data_pre.py
	引用：Movielens_ratings.txt
	结果：train\\Movielens_array_train_65%d.xlsx
		Movielens_ratings_test_241.txt
	用时：62s
Step2：
	目的：先划分测试集数据
	工具：ISA_test_method.py	import Test_split(t)	
	引用：train\\Movielens_ratings_test_65%d.txt		
	结果：eva\Movielens_isa_%d_%d_nmf_evaluate.xlsx
	用时：s
------------------------------------ISA聚类------------------------------
Step3：
	目的：ISA
	工具：Test_mtba_biclust.m (Matlab)
	引用：Movielens_array_train_242.xlsx
	结果：result_isa.m

Step4：	
	目的：主函数
	工具：ISA_51/52/61/62/71/72/.../.py	
Step4：
	目的：存储聚类矩阵总体信息及每个聚类的评分信息
	工具：ISA_method.py	import ISA_save
	注意：总矩阵无抬头，方便直接读入Matlab中，具体群组信息需要两文件配合使用
	引用：result_242_800.mat	(t,k)训练集编号，分组数
		Movielens_array_train_242.xlsx
	结果：Movielens_isa_242_780_sta.xlsx
		Movielens_isa_242_780_all.xlsx
	用时：254s
评分数据共  			35497条
分组覆盖结果：242	2000	780
分组覆盖结果：242	2000	800	181882	30545	4949
分组覆盖结果：242	2000	803	3346	23294	12200

-----------------------------------------------群组融合 专业度-------------------------
Step1：
	目的：计算群组评分均值（评分人数少于0.7，设为0）（或者可以设方差）------中位数-----ISA_mid_method.py(存储与7号机  ISA_user_6/mid)
	工具：ISA_weight_method.py		import ISA_group_weight
	引用：Movielens_isa_242_803_all.xlsx
		Movielens_isa_242_803_sta.xlsx
	结果：Movielens_isa_242_803_weight.xlsx
	用时：160s

Step4：
	目的：构建群组评分网络
	工具：ISA_net_method.py	import ISA_group_ave_net(t,k)
	引用：sta\\Movielens_isa_%d_%d_ave.xlsx
		sta\\Movielens_isa_%d_%d_sta.xlsx		
	结果：sta\\Movielens_isa_%d_%d_ave_net.xlsx
	用时：58s
Step3：
	目的：群组倒排档，计算并存储用户与每个群组的均值Virtual User Pearson相似度
	工具：ISA_inverted_method.py	import ISA_group_inverted	
	引用：sta\\Movielens_isa_%d_%d_ave_net.xlsx
		nmf\\Movielens_isa_%d_%d_all_nmf.xlsx
		sta\\Movielens_isa_%d_%d_sta.xlsx
		sta\\Movielens_isa_%d_%d_ave.xlsx
	结果：sta\Movielens_isa_%d_%d_inverted.xlsx
	用时：s
  -------------------以下弃用------------
Step3：
	目的：协同推荐
	工具：ISA_forecase_method.py 	import ISA_group_forecast
	引用：train\\Movielens_test_split_65%d.xlsx
		sta\\Movielens_isa_%d_%d_ave.xlsx
		sta\\Movielens_isa_%d_%d_ave_net.xlsx
		sta\Movielens_isa_%d_%d_inverted.xlsx
	结果：eva\\Movielens_isa_%d_%d_ave_forecast.xlsx
	用时：s
Step4：
	目的：Top-N推荐 nDCG评估
	工具：ISA_evaluation_method.py 	import ISA_group_evaluation	
	引用：train\\Movielens_test_split_%d.xlsx
		eva\\Movielens_isa_%d_%d_ave_forecast.xlsx
	结果：eva\\Movielens_isa_%d_%d_ave_nDCG.xlsx
	用时：15s

Step5:
	目的：最后统计所有nDCG结果，汇成一个表格
	工具：nDCG_all.py	def  nDCG_all
	引用：r'eva\\Movielens_isa_%d_%d_ave_nDCG.xlsx'%(t,k)
	结果：r'eva\\Movielens_isa_ave_nDCG_all.xlsx'
	用时：s
-------------------nDCG汇总-------------------------
Step1：
	目的：Top-N推荐 nDCG评估（设置推荐个数 10，20，30）
	工具：ISA_eva_method.py 	import ISA_group_eval	
	引用：train\\Movielens_test_split_%d.xlsx
		eva\\Movielens_isa_%d_%d_ave_forecast.xlsx
	结果：eva\\Movielens_isa_%d_%d_ave_nDCG.xlsx
	用时：15s

Step2:
	目的：最后统计所有nDCG结果，汇成一个表格
	工具：nDCG_n.py	def  nDCG_all
	引用：r'eva\\Movielens_isa_%d_%d_ave_nDCG.xlsx'%(t,k)
	结果：r'eva\\Movielens_isa_ave_nDCG_%d.xlsx'
	用时：s
------------------------------------MAE、RSME计算------------------------------
Step1：
	目的：计算目标用户与各虚拟群组用户的Pearson相似度
	工具：ISA_forecast_colla_method_6
	引用：E:/yao/MovieLens/sta_%d/Movielens_isa_%d_%d_all.xlsx
              E:/yao/MovieLens/sta_%d/Movielens_isa_%d_%d_weight.xlsx
	结果：E:/yao/MovieLens/sta_%d/Movielens_Pearson_%d_%d_weight.xlsx
	用时

Step2：
	目的：计算MAE、RSME(wrong)
	工具：MAE_RSME_eva_method.py	Eva(i)
	引用：E:/yao/MovieLens/eva_%d/Movielens_isa_%d_%d_weight_forecast.xlsx
              E:/yao/MovieLens/sta_%d/Movielens_isa_%d_%d_weight.xlsx
	结果：Movielens_isa_%d_mae_rsme.xlsx
	用时
Step3：
	目的：统计所有的MAE、RSME
	工具：ISA_fore_Colla_method.py(单独主函数)	
	引用：E:/yao/MovieLens/eva_%d/Movielens_isa_%d_%d_weight_forecast.xlsx
              E:/yao/MovieLens/train/Movielens_test_split_%d.xlsx
	结果：E:/yao/MovieLens/eva_%d/Movielens_isa_%d_weight_mae_rsme.xlsx
              Movielens_isa_weight_mae_rsme.xlsx
	用时
Step4：
	目的：统计所有的MAE、RSME
	工具：MAE_tongji.py(单独主函数)	
	引用：Movielens_isa_%d_mae_rsme.xlsx
	结果：Movielens_isa_weight_mae.xlsx
              Movielens_isa_weight_rsme.xlsx
	用时


