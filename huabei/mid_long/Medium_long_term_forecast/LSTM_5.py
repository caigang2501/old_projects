from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense


def lstm_procasting(df, length):
    # 读取 Excel 文件
    # df = pd.read_excel('09days_96p_price.xlsx', usecols=['data', 'price'])

    # 将日期列设为索引
    df.set_index('data', inplace=True)

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)

    # 定义时间窗口大小
    window_size = 24

    # 将数据集分为训练集和测试集，并分别归一化
    train_size = int(len(scaled_data) - window_size - length - 1)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size:]

    # 将数据集转换为时间序列数据
    def create_time_series(data, window_size):
        X = []
        y = []
        for i in range(window_size, len(data)):
            X.append(data[i - window_size:i])
            y.append(data[i])
        X, y = np.array(X), np.array(y)
        return X, y

    X_train, y_train = create_time_series(train_data, window_size)
    X_test, y_test = create_time_series(test_data, window_size)

    # 构建 LSTM 模型
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(window_size, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # 编译模型
    model.compile(optimizer='adam', loss='mean_squared_error')

    # 训练模型
    model.fit(X_train, y_train, batch_size=16, epochs=10)

    # 使用测试集进行预测
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    predictions = np.squeeze(predictions)
    predictions = np.delete(predictions, -1, 0)
    # predictions_df = pd.DataFrame({'Predictions': predictions})
    predictions_df = pd.DataFrame({'LSTM_Pred': predictions})

    def for_predict(data, model, pre_lengths, dim):
        """
        data:第一个给定的数据
        model:单步预测回归模型LSTM等
        pre_lengths:预测未来的步数
        dim:none,timesteps,dim中的dim维
        return: a ndarray that has pre_lengths elements
        """
        result = []
        init_sequence = data
        try:
            if data.shape == None or len(init_sequence.shape) != 3:
                raise TypeError('数据类型错误,必须为(none,timesteps,dim)')
        except TypeError as e:
            print('数据类型错误,必须为(none,timesteps,dim)')

        if dim == 1:
            for i in range(pre_lengths):
                pred = model(init_sequence).numpy()[0][0]
                init_sequence = init_sequence[0][1:]
                init_sequence = np.append(init_sequence, pred)
                init_sequence = init_sequence.reshape(1, 24, dim)
                result.append(pred)
            return np.array(result).reshape(-1, 1)
        if dim != 1:
            for i in range(pre_lengths):
                pred = model.predict(init_sequence).numpy()[0][:]
                init_sequence = init_sequence[0][1:]
                init_sequence = np.append(init_sequence, pred)
                init_sequence = init_sequence.reshape(1, 24, dim)
                result.append(pred)
            return np.array(result)

    dim = 1
    pre_lengths = length
    init_sequence = scaled_data[-25:-1].reshape(1, 24, dim)

    result = for_predict(init_sequence, model, pre_lengths, dim)
    forecast_df = scaler.inverse_transform(result)[:, 0]

    forecasts = np.squeeze(forecast_df)
    forecast_df = pd.DataFrame({'LSTM_Fore': forecasts})

    return predictions_df, forecast_df


""" # 绘制预测结果和实际结果的对比图
    plt.figure(figsize=(16, 8))
    plt.plot(df.index[train_size + window_size:], predictions, label='Predictions')
    plt.plot(df.index[train_size + window_size:],
             scaler.inverse_transform(y_test), label='Actual')
    plt.legend()
    plt.show()"""

    # actual_df = pd.DataFrame(scaler.inverse_transform(
        # y_test), index=df.index[train_size + window_size:], columns=['Actual'])

    # 将预测值和实际值保存到 Excel 文件中
    # result_df = pd.concat([predictions_df, actual_df], axis=1)
    # result_df.to_excel('result.xlsx', sheet_name='LSTM', index=True)

    # 训练模型并记录历史损失数据
    # history = model.fit(X_train, y_train, batch_size=64, epochs=50, verbose=0)

""" #######################
    # 6.MAPE和SMAPE.

    def mape(y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_pred - y_true) / y_true)) * 100

    MAPE = mape(actual_df, predictions_df)  # actual_df为实际值，predictions_df为预测值

    r2 = r2_score(y_true=actual_df, y_pred=predictions_df)

    # 决定系数，反映的是模型的拟合程度，R2的范围是0到1。
    # 其值越接近1，表明方程的变量对y的解释能力越强，这个模型对数据拟合的也较好。
    print("MAE=", mean_absolute_error(actual_df, predictions_df))
    print("RMSE=", np.sqrt(mean_squared_error(actual_df, predictions_df)))
    print("MAPE=", MAPE)
    print("R2=", r2)
    print(predictions_df)
    print(actual_df)
    # 绘制损失图
    plt.plot(history.history['loss'])
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show()"""



