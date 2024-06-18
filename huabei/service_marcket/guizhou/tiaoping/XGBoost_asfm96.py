# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 23:10:27 2023

@author: Moomin
"""

from xgboost import XGBRegressor
from xgboost import plot_importance
from matplotlib import pyplot
import pandas as pd
import os
def xgboost(path):
#if __name__ == '__main__':
#    path = './现货.xlsx'
    df = pd.read_excel(path, usecols=['load', 'temperature', 'wind_speed', 'price'])
    Y = df['price']
    Y = Y.drop(Y.tail(192).index)
    X = df.drop(['price'],axis=1)
    X = X.drop(X.tail(192).index)
    
    df2 = df.tail(192)
    X2 = df2.drop(['price'],axis=1)
    
    model = XGBRegressor(max_depth=6,          # 每一棵树最大深度，默认6；
                            learning_rate=0.01,      # 学习率，每棵树的预测结果都要乘以这个学习率，默认0.3；
                            n_estimators=100,        # 使用多少棵树来拟合，也可以理解为多少次迭代。默认100；
                            objective='reg:linear',   # 此默认参数与 XGBClassifier 不同
                            booster='gbtree',         # 有两种模型可以选择gbtree和gblinear。gbtree使用基于树的模型进行提升计算，gblinear使用线性模型进行提升计算。默认为gbtree
                            gamma=0,                 # 叶节点上进行进一步分裂所需的最小"损失减少"。默认0；
                            min_child_weight=1,      # 可以理解为叶子节点最小样本数，默认1；
                            subsample=1,              # 训练集抽样比例，每次拟合一棵树之前，都会进行该抽样步骤。默认1，取值范围(0, 1]
                            colsample_bytree=1,       # 每次拟合一棵树之前，决定使用多少个特征，参数默认1，取值范围(0, 1]。
                            reg_alpha=0,             # 默认为0，控制模型复杂程度的权重值的 L1 正则项参数，参数值越大，模型越不容易过拟合。
                            reg_lambda=1,            # 默认为1，控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
                            random_state=0)           # 随机种子
    
    model.fit(X,Y)
    Y_2 = list(model.predict(X2))
    Y_test = Y_2[:96]
    Y_pred = Y_2[96:192]
    pd.DataFrame(Y_test).to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_XGBoost_test.xlsx'), index=False, header=False)
    pd.DataFrame(Y_pred).to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_XGBoost_pred.xlsx'), index=False, header=False)

