from PyEMD.CEEMDAN import CEEMDAN
import numpy as np
import pandas as pd
import warnings
from matplotlib import pyplot as plt
from product_elic.Forecasting import ARIMA, Exponential_Smoothing_96
import os

warnings.filterwarnings(action='ignore')


def run_model(history_path):
    his_df = pd.read_excel(history_path, usecols=['price'])

    train_size = int(len(his_df) - 96)     # 预测数据的长度
    test_data_size = his_df[train_size:]

    train_data = his_df[:train_size]
    test_data = his_df[train_size:]

    print('Prepare to run the ARIMA algorithm')
    ARIMA_test, ARIMA_predict = ARIMA.arima_procasting(train_data.values, test_data.values)

    print('Prepare to run the LSTM algorithm')
    lstm_data = pd.read_excel(history_path, usecols=['data', 'price'])
    # LSTM_test, LSTM_predict, = LSTM_96.lstm_procasting(lstm_data)

    print('Prepare to run the Exponential Smoothing algorithm')
    train_data = his_df[:train_size]
    SES_test = Exponential_Smoothing_96.single_exp_smoothing(train_data)
    SES_predict = Exponential_Smoothing_96.single_exp_smoothing(his_df)

    # 测试值
    ARIMA_test.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_ARIMA_test.xlsx'), index=False, header=False)
    # LSTM_test.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_LSTM_test.xlsx'), index=False, header=False)
    SES_test.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_SES_test.xlsx'), index=False, header=False)

    # 预测值
    ARIMA_predict.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_ARIMA_pred.xlsx'), index=False, header=False)
    # LSTM_predict.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_LSTM_pred.xlsx'), index=False, header=False)
    SES_predict.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/96_SES_pred.xlsx'), index=False, header=False)


