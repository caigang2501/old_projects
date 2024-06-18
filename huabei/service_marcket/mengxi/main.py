# -*- coding: utf-8 -*-
#辅助服务市场用到的库
from service_marcket.mengxi import Transformer_asfm,GABPNet_asfm,XGBoost_asfm,com_xlsx_asfm,Auxiliary_service_asfm
import pandas as pd
import requests
######################################################################################
def main(path_asfm):
    """辅助服务市场"""
    """调频市场报价"""
    Transformer_asfm.transformer(path_asfm)
    print('run transformer over')
    GABPNet_asfm.gabpnet(path_asfm)
    print('run gabpnet over')
    XGBoost_asfm.xgboost(path_asfm)
    # decom_price_test_pred_asfm.run_model(path_asfm)
    # test_asfm, predict_asfm = com_xlsx_asfm.comxlsx(path_asfm)
    #输出
    ##################################################################
    print('*****************辅助服务市场市场*******************')
    """调频市场报价"""
    """调频竞价交易"""
    # 是否谋求成为边际机组: 0 ----> 否； 1 ----> 是
    asfm_marginal_unit = 1
    return Auxiliary_service_asfm.midlong(asfm_marginal_unit)

if __name__=='__main__':
    main('history_asfm_50_220107_231110.xlsx')