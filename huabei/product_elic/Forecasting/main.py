# -*- coding: utf-8 -*-
from product_elic.Forecasting import decom_price_test_pred_96,Transformer_96,GABPNet_96,XGBoost_96,com_xlsx,COM_Fore_Price
import pandas as pd

import requests
import os

def main(path_96):
    Transformer_96.transformer(path_96)
    print('run transformer over')
    GABPNet_96.gabpnet(path_96)

    print('run gabpnet over')
    XGBoost_96.xgboost(path_96)
    print('run xgboost over')
    decom_price_test_pred_96.run_model(path_96)     # CEEMDAN + ARIMA 测试和预测输出
    # print('run decom_price_test_pred_96 over')
    """合并结果"""
    test_96, predict_96 = com_xlsx.comxlsx(path_96)

    npoints_test, npoints_pred = os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_test.xlsx'), os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_predict.xlsx')
    (day_ahead_fore,error_com)   = COM_Fore_Price.com_fore_price(npoints_test, npoints_pred)
    pd.DataFrame(day_ahead_fore).to_excel(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'Strategy/final_predict.xlsx'), index=False, header=False)
    # print("现货日前价格-----组合预测价格误差为: ",error_com* 100,'%')
    # print("现货日前价格-----组合预测价格: ", day_ahead_fore)
    return day_ahead_fore # leng=96的数组

if __name__=='__main__':
    print('result => ',main("现货.xlsx"))
