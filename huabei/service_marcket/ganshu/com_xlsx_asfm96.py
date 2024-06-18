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
    
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_GABPNet_test.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_XGBoost_test.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_Transformer_test.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_ARIMA_test.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_LSTM_test.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_SES_test.xlsx'), header=None).iloc[:, 0])
    
    D1 = pd.DataFrame({'original': original, 'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D1.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_test.xlsx'), index=False)
    
    #####96_pred
    GABPNet = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_GABPNet_pred.xlsx'), header=None).iloc[:, 0])
    XGBoost = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_XGBoost_pred.xlsx'), header=None).iloc[:, 0])
    Transformer = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_Transformer_pred.xlsx'), header=None).iloc[:, 0])
    ARIMA = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_ARIMA_pred.xlsx'), header=None).iloc[:, 0])
    LSTM = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_LSTM_pred.xlsx'), header=None).iloc[:, 0])
    SES = list(pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_SES_pred.xlsx'), header=None).iloc[:, 0])
    
    D2 = pd.DataFrame({'ARIMA': ARIMA, 'LSTM': LSTM, 'SES': SES, 'XGBoost': XGBoost,
                       'Transformer': Transformer, 'GABPNet': GABPNet})
    D2.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_predict.xlsx'), index=False)
   
    return D1, D2



