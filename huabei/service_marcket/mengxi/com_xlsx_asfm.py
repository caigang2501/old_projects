# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 19:16:50 2023

@author: Moomin
"""
import pandas as pd
import os

def comxlsx(path_6):
    #####5_test
    df = pd.read_excel(path_6, usecols=['price']).tail(10)
    original = list(df['price'])[:5]
    
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_GABPNet_test.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_XGBoost_test.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_Transformer_test.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_ARIMA_test.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_LSTM_test.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_SES_test.xlsx'), header=None).iloc[:, 0])
    
    D1 = pd.DataFrame({'original': original, 'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D1.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_test.xlsx'), index=False)
    
    
    #####5_pred
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_GABPNet_pred.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_XGBoost_pred.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_Transformer_pred.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_ARIMA_pred.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_LSTM_pred.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_SES_pred.xlsx'), header=None).iloc[:, 0])
    
    D2 = pd.DataFrame({'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D2.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_predict.xlsx'), index=False)
    
    
    return D1, D2



