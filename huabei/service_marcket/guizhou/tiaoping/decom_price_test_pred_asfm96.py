from PyEMD.CEEMDAN import CEEMDAN
import numpy as np
import pandas as pd
import warnings
from matplotlib import pyplot as plt
from service_marcket.guizhou.tiaoping import ARIMA, LSTM_asfm96, Exponential_Smoothing_asfm96


warnings.filterwarnings(action='ignore')  # 忽略告警


def run_model(history_path):
    # CEEMDAN价格分解
    def ceemdan_decompose(data):
        ceemdan = CEEMDAN()
        ceemdan.ceemdan(data)
        imfs, res = ceemdan.get_imfs_and_residue()
        plt.figure(figsize=(12, 9))
        plt.subplots_adjust(hspace=0.1)
        plt.subplot(imfs.shape[0] + 2, 1, 1)
        plt.plot(data, 'r')
        for i in range(imfs.shape[0]):
            plt.subplot(imfs.shape[0] + 2, 1, i + 2)
            plt.plot(imfs[i], 'g')
            plt.ylabel("IMF %i" % (i + 1))
            plt.locator_params(axis='x', nbins=10)
            IImfs.append(imfs[i])


    his_df = pd.read_excel(history_path)
    IImfs = []
    ceemdan_decompose(np.array(his_df['price'].values).ravel())     # IImfs = [6/7/8/9, 2976]
    IImfs = np.transpose(IImfs)     # IImfs = [2976, 6/7/8/9]
    vec = pd.DataFrame(IImfs)
    price_decom = his_df['data']
    for i in range(IImfs.shape[1]):
        price_decom = pd.concat([price_decom, vec.iloc[:, i]], axis=1)
    price_decom.to_excel('price_decom_asfm96.xlsx', sheet_name='decom', index=False)     # CEEMDAN价格分解文件
    # 'price_decom.xlsx'----> columns: data, 0-->6/7/8/9-1

    train_size = int(len(vec) - 96)  # 预测数据的长度
    test_data_size = his_df[train_size:]
    decom_test_result = pd.DataFrame(data=None, index=range(0, 96, 1))
    decom_predict_result = pd.DataFrame(data=None, index=range(0, 96, 1))

    print('Prepare to run the ARIMA algorithm')
    for i in range(1, 4):
        vec_ari = pd.read_excel('price_decom_asfm96.xlsx')
        test_vec = vec_ari.iloc[:, i]
        train_data = test_vec[:train_size]
        test_data = test_vec[train_size:]
        ARIMA_test_result, ARIMA_predict_result = ARIMA.arima_procasting(train_data.values, test_data.values)
        decom_test_result = pd.concat([decom_test_result, ARIMA_test_result], axis=1)
        decom_predict_result = pd.concat([decom_predict_result, ARIMA_predict_result], axis=1)

    print('Prepare to run the LSTM algorithm')
    for i in range(1, 4):
        vec_lstm = pd.read_excel('price_decom_asfm96.xlsx', usecols=[0, i])
        LSTM_test_result, LSTM_forcast_result, = LSTM_asfm96.lstm_procasting(vec_lstm)
        decom_test_result = pd.concat([decom_test_result, LSTM_test_result], axis=1)
        decom_predict_result = pd.concat([decom_predict_result, LSTM_forcast_result], axis=1)

    print('Prepare to run the Exponential Smoothing algorithm')
    for i in range(1, 4):
        vec_ses = pd.read_excel('price_decom_asfm96.xlsx')
        test_vec = vec_ses.iloc[:, i]
        train_data = test_vec[:train_size]
        decom_test_result = pd.concat([decom_test_result, Exponential_Smoothing_asfm96.single_exp_smoothing(train_data)],
                                      axis=1)
        decom_predict_result = pd.concat([decom_predict_result, Exponential_Smoothing_asfm96.single_exp_smoothing(test_vec)],
                                      axis=1)

    # decom_test_result.to_excel('decom_test_result.xlsx')  # 价格分解前三维向量测试结果 ----> data + ARIMA*3 + LSTM*3 + SES*3
    # decom_predict_result.to_excel('decom_predict_result.xlsx')  # 价格分解前三维向量预测结果

    test_result = pd.DataFrame(data=None, index=range(0, 96, 1))
    predict_result = pd.DataFrame(data=None, index=range(0, 96, 1))

    decom_sum = []
    for i in range(train_size, IImfs.shape[0]):  # IImfs = [2976+1, 9+1]
        vec_sum = np.sum(IImfs[i, :])  # 按行求和
        decom_sum.append(vec_sum)  # decom_sum = [2976, 1] 后6维的和
    decom_sum = np.array(decom_sum)

    ave = np.mean(decom_sum)

    # 测试值
    ARIMA_test = pd.DataFrame({'ARIMA_test': decom_test_result.iloc[:, 0] +
                                             decom_test_result.iloc[:, 1] +
                                             decom_test_result.iloc[:, 2] + decom_sum})
    LSTM_test = pd.DataFrame({'LSTM_test': decom_test_result.iloc[:, 3] +
                                           decom_test_result.iloc[:, 4] +
                                           decom_test_result.iloc[:, 5] + decom_sum})
    SES_test = pd.DataFrame({'SES_test': decom_test_result.iloc[:, 6] +
                                         decom_test_result.iloc[:, 7] +
                                         decom_test_result.iloc[:, 8] + decom_sum})

    ARIMA_test.to_excel('./result/asfm96_ARIMA_test.xlsx', index=False, header=False)
    LSTM_test.to_excel('./result/asfm96_LSTM_test.xlsx', index=False, header=False)
    SES_test.to_excel('./result/asfm96_SES_test.xlsx', index=False, header=False)

    # 预测值
    ARIMA_predict = pd.DataFrame({'ARIMA_test': decom_predict_result.iloc[:, 0] +
                                                decom_predict_result.iloc[:, 1] +
                                                decom_predict_result.iloc[:, 2] + ave})
    LSTM_predict = pd.DataFrame({'LSTM_test': decom_predict_result.iloc[:, 3] +
                                              decom_predict_result.iloc[:, 4] +
                                              decom_predict_result.iloc[:, 5] + ave})
    SES_predict = pd.DataFrame({'SES_test': decom_predict_result.iloc[:, 6] +
                                            decom_predict_result.iloc[:, 7] +
                                            decom_predict_result.iloc[:, 8] + ave})

    ARIMA_predict.to_excel('./result/asfm96_ARIMA_pred.xlsx', index=False, header=False)
    LSTM_predict.to_excel('./result/asfm96_LSTM_pred.xlsx', index=False, header=False)
    SES_predict.to_excel('./result/asfm96_SES_pred.xlsx', index=False, header=False)


