# -*- coding: utf-8 -*-

#辅助服务市场用到的库
from service_marcket.guizhou.tiaoping import Transformer_asfm96,GABPNet_asfm96,XGBoost_asfm96,com_xlsx_asfm96,Auxiliary_service_asfm96
import requests
import pandas as pd
######################################################################################
def main(path_asfm96):
    Transformer_asfm96.transformer(path_asfm96)
    print('run transformer over')
    GABPNet_asfm96.gabpnet(path_asfm96)
    print('run gabpnet over')
    XGBoost_asfm96.xgboost(path_asfm96)
    # decom_price_test_pred_asfm96.run_model(path_asfm96)
    test_asfm96, predict_asfm96 = com_xlsx_asfm96.comxlsx(path_asfm96)
    #输出
    ##################################################################

    ################################################################
    print('*****************辅助服务市场市场*******************')

    """调频市场报价"""
    return Auxiliary_service_asfm96.asfm96() #leng=24的数组

if __name__=='__main__':
    pass