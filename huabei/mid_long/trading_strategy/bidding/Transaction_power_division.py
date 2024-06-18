"""
深度调峰竞价交易
"""
import numpy as np
import pandas as pd

def midlong():  
 
    # 从Excel文件读取数据
    tpd = pd.read_excel(io='./电量比例划分.xlsx', header=0)
    power_amof24 = pd.read_excel(io='./input_power.xlsx', sheet_name='年度逐月24时段出力预测', header=0)
    power_bn24 = pd.read_excel(io='./input_power.xlsx', sheet_name='年度逐月24时段双边协商签约情况', header=0)
    power_bnm24 = pd.read_excel(io='./input_power.xlsx', sheet_name='月度24时段双边协商签约情况', header=0)
    # power_d = pd.read_excel(io='./input_power.xlsx', sheet_name='月度24时段双边协商签约情况', header=0)
    # 将数据框转换为NumPy数组
    tpd = tpd.values
    power_amof24 = np.array(power_amof24)
    power_bn24 = np.array(power_bn24)
    power_bnm24 = np.array(power_bnm24)
    #中长期年度电量
    mlae_max = tpd[0,0]*tpd[0,1]+tpd[0,0]*(1-tpd[0,3])*(tpd[0,4]/(tpd[0,4]+tpd[0,8]))*(tpd[0,5]/(tpd[0,5]+tpd[0,6]+tpd[0,7]))
    mlae_min = tpd[1,0]*tpd[0,1]+tpd[1,0]*(1-tpd[0,3])*(tpd[0,4]/(tpd[0,4]+tpd[0,8]))*(tpd[0,5]/(tpd[0,5]+tpd[0,6]+tpd[0,7]))
    #中长期月度电量
    mlme_max = tpd[0,0]*(tpd[0,2]-tpd[0,1])+tpd[0,0]*(1-tpd[0,3])*(tpd[0,4]/(tpd[0,4]+tpd[0,8]))*(tpd[0,6]/(tpd[0,5]+tpd[0,6]+tpd[0,7]))
    mlme_min = tpd[1,0]*(tpd[0,2]-tpd[0,1])+tpd[1,0]*(1-tpd[0,3])*(tpd[0,4]/(tpd[0,4]+tpd[0,8]))*(tpd[0,6]/(tpd[0,5]+tpd[0,6]+tpd[0,7]))
    #中长期月内电量
    mlmde_max = tpd[0,0]*(tpd[0,3]-tpd[0,2])+tpd[0,0]*(1-tpd[0,3])*(tpd[0,4]/(tpd[0,4]+tpd[0,8]))*(tpd[0,7]/(tpd[0,5]+tpd[0,6]+tpd[0,7]))
    mlmde_min = tpd[1,0]*(tpd[0,3]-tpd[0,2])+tpd[1,0]*(1-tpd[0,3])*(tpd[0,4]/(tpd[0,4]+tpd[0,8]))*(tpd[0,7]/(tpd[0,5]+tpd[0,6]+tpd[0,7]))
    #现货电量
    se_max = tpd[0,0]*(1-tpd[0,3])*(tpd[0,8]/(tpd[0,4]+tpd[0,8]))
    se_min = tpd[1,0]*(1-tpd[0,3])*(tpd[0,8]/(tpd[0,4]+tpd[0,8]))
    
    # p_mlae_max = mlae_max/tpd[0,0]
    # p_mlme_max = mlme_max/tpd[0,0]
    # p_mlmde_max = mlmde_max/tpd[0,0]
    # p_se_max = se_max/tpd[0,0]
    p_mlae_min = mlae_min/tpd[1,0]
    p_mlme_min = mlme_min/tpd[1,0]
    p_mlmde_min = mlmde_min/tpd[1,0]
    p_se_min = se_min/tpd[1,0]
    #年度集中竞价电量-->扣减掉签好的双边协商电量，得到年度集中竞价的12个月各月24时段交易电量
    power_cb = power_amof24[:,1:25] * p_mlae_min - power_bn24[:,1:25]
    #月度集中竞价电量
    power_cbm = power_amof24[:,1:25] * p_mlme_min -power_bnm24[:,1:25]
    # 结果
    print("*******最大电量划分**********")     
    print("中长期年度电量 中长期月度电量 中长期月内电量 现货电量：", mlae_max,mlme_max,mlmde_max,se_max)
    # print("中长期年度电量比例 中长期月度电量比例 中长期月内电量比例 现货电量比例：", p_mlae_max.round(2)*100,'%',p_mlme_max.round(2)*100,'%',p_mlmde_max.round(2)*100,'%',p_se_max.round(2)*100,'%')
    print("*******最小电量划分**********")     
    print("中长期年度电量 中长期月度电量 中长期月内电量 现货电量：", mlae_min,mlme_min,mlmde_min,se_min)
    print("中长期年度电量比例 中长期月度电量比例 中长期月内电量比例 现货电量比例：", p_mlae_min.round(4)*100,'%',p_mlme_min.round(4)*100,'%',p_mlmde_min.round(4)*100,'%',p_se_min.round(4)*100,'%')
    print("*******年度集中竞价1-12月各月签约电量**********") 
    print(power_cb)
    print("*******月度集中竞价1-12月各月签约电量**********") 
    print(power_cbm)
midlong()
























