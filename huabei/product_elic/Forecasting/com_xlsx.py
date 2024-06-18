# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 19:16:50 2023

@author: Moomin
"""
import pandas as pd
import os


def comxlsx(path_96):
    #####96_test
    df = pd.read_excel(path_96, usecols=['price']).tail(192)
    original = list(df['price'])[:96]
    
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_GABPNet_test.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_XGBoost_test.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_Transformer_test.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_ARIMA_test.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_LSTM_test.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_SES_test.xlsx'), header=None).iloc[:, 0])
    
    D3 = pd.DataFrame({'original': original, 'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D3.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_test.xlsx'), index=False)
    
    #####96_pred
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_GABPNet_pred.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_XGBoost_pred.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_Transformer_pred.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_ARIMA_pred.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_LSTM_pred.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_SES_pred.xlsx'), header=None).iloc[:, 0])
    
    D4 = pd.DataFrame({'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D4.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_predict.xlsx'), index=False)
    
    return D3, D4