"""
中长期竞价交易
"""
import pandas as pd
import numpy as np
import os
"""中长期竞价交易"""
# 是否谋求成为边际机组: 0 ----> 否； 1 ----> 是
#marginal_unit = 1

# # 竞价电量总量
# total_power = 1000
    
# # 竞价电量比例 ----> 光伏, 风电, 燃煤
# unit_compete_ratio = np.array([0.2, 0.3, 0.5])

# # 各机组类型度电成本 ----> 光伏, 风电, 燃煤
# unit_per_cost = np.array([300, 300, 298])
def main(path):
    data_df = pd.read_excel(path, sheet_name='DATA', header=0)
    (total_power, unit_compete_ratio1,unit_compete_ratio2,unit_compete_ratio3,
    unit_per_cost1,unit_per_cost2,unit_per_cost3) = data_df.iloc[0]
    unit_compete_ratio =np.array([unit_compete_ratio1,unit_compete_ratio2,unit_compete_ratio3])
    unit_per_cost = np.array([unit_per_cost1,unit_per_cost2,unit_per_cost3])
    # 竞价电量加权平均度电成本
    per_cost = np.sum((unit_compete_ratio * total_power) * unit_per_cost) / total_power

    mid_long_fore = list(pd.read_excel('5_com_pred.xlsx', header=None).iloc[:, 0])

    return {'seek':mid_long_fore[1:6],'noseek':per_cost}


if __name__=='__main__':
    result = main('input_data.xlsx')
    print("谋求成为边际机组策略下中长期竞价报价：", result['seek'])
    print("不谋求成为边际机组策略下中长期竞价报价：", result['noseek'])






















