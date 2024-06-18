from statsmodels.tsa.stattools import adfuller
import pandas as pd
# import matplotlib.pyplot as plt
import statsmodels.api as sm
import itertools
import numpy as np
# import warnings
# import seaborn as sns


def arima_procasting(train_data, test_data, length):
    # 创建一个函数来检查数据的平稳性
    def test_stationarity(timeseries):
        # 执行Dickey-Fuller测试
        # print('Results of Dickey-Fuller Test:')
        dftest = adfuller(timeseries, autolag='AIC')
        dfoutput = pd.Series(dftest[0:length-1], index=[
            'Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
        for key, value in dftest[length-1].items():
            dfoutput['Critical Value (%s)' % key] = value
        # print(dfoutput)

    # data_input_1 = np.diff(np.transpose(df['price'].values), n=1)     # 一阶差分
    # ata_input_2 = np.diff(np.transpose(data_input_1), n=1)     # 二阶差分
    # origin_series = np.expand_dims(df['price'].values, axis=1)
    # test_stationarity(origin_series)
    # test_stationarity(data_input_1)
    # test_stationarity(data_input_2)

    # """ 数据平稳性检查
    # Results of Dickey-Fuller Test:
    # Test Statistic                -6.856025e+00
    # p-value                        1.647663e-09
    # #Lags Used                     2.400000e+01
    # Number of Observations Used    2.951000e+03
    # Critical Value (1%)           -3.432568e+00
    # Critical Value (5%)           -2.862520e+00
    # Critical Value (10%)          -2.567292e+00
    # dtype: float64
    # Results of Dickey-Fuller Test:
    # Test Statistic                -1.576066e+01
    # p-value                        1.192806e-28
    # #Lags Used                     2.700000e+01
    # Number of Observations Used    2.947000e+03
    # Critical Value (1%)           -3.432571e+00
    # Critical Value (5%)           -2.862521e+00
    # Critical Value (10%)          -2.567292e+00
    # dtype: float64
    # Results of Dickey-Fuller Test:
    # Test Statistic                  -24.347797
    # p-value                           0.000000
    # #Lags Used                       29.000000
    # Number of Observations Used    2944.000000
    # Critical Value (1%)              -3.432573
    # Critical Value (5%)              -2.862522
    # Critical Value (10%)             -2.567293
    # dtype: float64"""

    # # 参数确定
    # fig = plt.figure(figsize=(12, 7))

    # ax1 = fig.add_subplot(211)
    # fig = sm.graphics.tsa.plot_acf(train_data, lags=20, ax=ax1)
    # # 设置坐标轴上的数字显示的位置，top:显示在顶部  bottom:显示在底部
    # ax1.xaxis.set_ticks_position('bottom')
    # # fig.tight_layout()

    # ax2 = fig.add_subplot(212)
    # fig = sm.graphics.tsa.plot_pacf(train_data, lags=20, ax=ax2)
    # ax2.xaxis.set_ticks_position('bottom')
    # # fig.tight_layout()
    # # plt.show()

    # 确定pq的取值范围
    p_min = 0
    d_min = 0
    q_min = 0
    p_max = 2
    d_max = 0
    q_max = 2
    # Initialize a DataFrame to store the results,，以BIC准则
    results_bic = pd.DataFrame(index=['AR{}'.format(i) for i in range(p_min, p_max + 1)],
                               columns=['MA{}'.format(i) for i in range(q_min, q_max + 1)])

    for p, d, q in itertools.product(range(p_min, p_max + 1),
                                     range(d_min, d_max + 1),
                                     range(q_min, q_max + 1)):
        if p == 0 and d == 0 and q == 0:
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = np.nan
            continue
        try:
            model = sm.tsa.ARIMA(train_data, order=(p, d, q),
                                 # enforce_stationarity=False,
                                 # enforce_invertibility=False,
                                 )
            results = model.fit()
            results_bic.loc['AR{}'.format(p), 'MA{}'.format(q)] = results.bic
        except:
            continue
    results_bic
    # 得到结果后进行浮点型转换
    results_bic = results_bic[results_bic.columns].astype(float)
    # # 绘制热力图
    # fig, ax = plt.subplots(figsize=(10, 8))
    # ax = sns.heatmap(results_bic,
    #                  mask=results_bic.isnull(),
    #                  ax=ax,
    #                  annot=True,
    #                  fmt='.2f',
    #                  cmap="Purples"
    #                  )

    # ax.set_title('BIC')
    # plt.show()
    results_bic.stack().idxmin()
    # 利用模型取p和q的最优值
    # train_results = sm.tsa.arma_order_select_ic(
    #     train_data, ic=['aic', 'bic'], trend='n', max_ar=8, max_ma=8)

    # print('AIC', train_results.aic_min_order)
    # print('BIC', train_results.bic_min_order)
    # 模型检验
    p = 1
    d = 0
    q = 2
    model = sm.tsa.ARIMA(test_data, order=(p, d, q))
    results = model.fit()
    # resid = results.resid  # 获取残差
    # 查看测试集的时间序列与数据(只包含测试集)
    # fig, ax = plt.subplots(figsize=(12, 5))
    # ax = sm.graphics.tsa.plot_acf(resid, lags=5, ax=ax)
    # plt.show()

    # 模型预测
    # results.predict(start=len(train), end=len(train) + len(test) - 1, dynamic=False)
    predict_sunspots = results.predict(dynamic=False)
    # results.forecast(steps=len(test))  # predict(dynamic=False)
    # print(predict_sunspots)

    # """# 查看测试集的时间序列与数据(只包含测试集)
    # plt.figure(figsize=(12, 6))
    # plt.plot(test_data['price'].values)
    # plt.xticks(rotation=45)  # 旋转45度
    # plt.plot(predict_sunspots)
    # # plt.show()"""

    # """# 绘图
    # fig, ax = plt.subplots(figsize=(12, 6))
    # ax = plt.plot(ax=ax)
    # # 预测数据
    # plt.plot(predict_sunspots)
    # # plt.show()"""

    # print(test_data['data'].values.shape, test_data['price'].values.shape, predict_sunspots.shape)
    # 创建两个DataFrame，将时间序列数据存储在其中
    # sub_df = pd.DataFrame({'Date': test_data['data'].values, 'SubData': test_data['price'].values})
    predict_df = pd.DataFrame(
        {'ARIMA_Pred': predict_sunspots})

    # 合并两个DataFrame，使用外连接以保留所有日期
    # pred_result = pd.merge(sub_df, predict_df)

    # 将NaN填充为适当的值（如果需要）
    predict_df = predict_df.fillna(0)  # 这里将缺失的值填充为0，可以根据需求进行更改

    ##############################
    # test = sub.loc['2022-04-30 0:49:46':'2022-04-30 22:59:46']
    # forecast_steps = 24  # 例如，预测未来24个时间步的值
    # print(results.forecast(steps=forecast_steps))
    # 使用训练好的ARIMA模型进行预测
    # 使用模型对测试集数据进行预测
    forecast = results.forecast(steps=len(test_data))

    # 创建一个日期时间索引
    # data_range = pd.date_range(start='2023/2/1 00:00', end='2023/2/1 23:45', freq='15MIN')

    # 将日期时间索引与预测值合并成一个新的DataFrame
    forecast_df = pd.DataFrame({'ARIMA_Fore': forecast})
    # 将DataFrame保存到Excel文件
    # predicted_df.to_excel('output.xlsx', index=False)

    # 打印包含预测和时间信息的DataFrame
    # print(predicted_df)
    return predict_df, forecast_df



