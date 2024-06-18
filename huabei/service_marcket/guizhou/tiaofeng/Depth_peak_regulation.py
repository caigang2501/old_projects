"""
深度调峰竞价交易
"""
import numpy as np
import pandas as pd

def midlong(path):
 
    # unit_compete_ratio = np.array([[0.2, 0.3, 0.5],[0.2, 0.3, 0.5],[0.2, 0.3, 0.5]])
    # unit_per_cost = np.array([[0.067, 0.045, 0.081],[0.456, 0.245, 0.648],[0.758, 0.648, 0.972]])
    
    # 从Excel文件读取数据
    # 参与不同档位调峰机组负荷率比例 ----> 光伏, 风电, 燃煤
    unit_compete_ratio_df = pd.read_excel(path, sheet_name='unit_compete_ratio', header=None)
    # 各机组类型不同调峰档位度电成本 ----> 光伏, 风电, 燃煤
    unit_per_cost_df = pd.read_excel(path, sheet_name='unit_per_cost', header=None)

    # 将数据框转换为NumPy数组
    unit_compete_ratio = unit_compete_ratio_df.values
    unit_per_cost = unit_per_cost_df.values
    # 竞价电量加权平均度电成本
    per_cost = np.sum(unit_compete_ratio * unit_per_cost, axis=1)
    return per_cost
if __name__=='__main__':
    print("*******深度调峰三档报价**********")
    print("第一档 第二档 第三档：", midlong('./input_data.xlsx'))

























