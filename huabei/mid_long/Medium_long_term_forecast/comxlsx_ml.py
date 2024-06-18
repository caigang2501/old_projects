# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 19:16:50 2023

@author: Moomin
"""
import pandas as pd
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mid_long/Medium_long_term_forecast'))


def comxlsx(path_5, length):
    #####5_test
    df = pd.read_excel(path_5, usecols=['price']).tail(length * 2)
    original = list(df['price'])[:length]
    
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_GABPNet_test.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_XGBoost_test.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_Transformer_test.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_ARIMA_test.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_LSTM_test.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_SES_test.xlsx'), header=None).iloc[:, 0])
    
    D1 = pd.DataFrame({'original': original, 'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D1.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_test.xlsx'), index=False)
    
    
    #####5_pred
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_GABPNet_pred.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_XGBoost_pred.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_Transformer_pred.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_ARIMA_pred.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_LSTM_pred.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_SES_pred.xlsx'), header=None).iloc[:, 0])
    
    D2 = pd.DataFrame({'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D2.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_predict.xlsx'), index=False)
    
 
    return D1, D2



