from PyEMD.CEEMDAN import CEEMDAN
import numpy as np
import pandas as pd
import warnings
from matplotlib import pyplot as plt
from mid_long.Medium_long_term_forecast import ARIMA, Exponential_Smoothing_5
import os
warnings.filterwarnings(action='ignore')  # 忽略告警


def run_model(history_path, length):
    his_df = pd.read_excel(history_path, usecols=['price'])

    train_size = int(len(his_df) - length)     # 预测数据的长度
    train_data = his_df[:train_size]
    test_data = his_df[train_size:]

    print('Prepare to run the ARIMA algorithm')
    ARIMA_test, ARIMA_predict = ARIMA.arima_procasting(train_data.values, test_data.values, length=length)

    print('Prepare to run the LSTM algorithm')
    lstm_data = pd.read_excel(history_path, usecols=['data', 'price'])
    # LSTM_test, LSTM_predict = LSTM_5.lstm_procasting(lstm_data, length=length)

    print('Prepare to run the Exponential Smoothing algorithm')
    SES_test = Exponential_Smoothing_5.single_exp_smoothing(train_data, length=length)
    SES_predict = Exponential_Smoothing_5.single_exp_smoothing(his_df, length=length)

    # 测试值
    ARIMA_test.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_ARIMA_test.xlsx'), index=False, header=False)
    # LSTM_test.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_LSTM_test.xlsx'), index=False, header=False)
    SES_test.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_SES_test.xlsx'), index=False, header=False)

    # 预测值
    ARIMA_predict.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_ARIMA_pred.xlsx'), index=False, header=False)
    # LSTM_predict.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_LSTM_pred.xlsx'), index=False, header=False)
    SES_predict.to_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_SES_pred.xlsx'), index=False, header=False)


