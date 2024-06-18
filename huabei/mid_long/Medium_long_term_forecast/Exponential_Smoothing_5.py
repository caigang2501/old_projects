import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, median_absolute_error
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# Single Exponential Smoothing
# https://blog.csdn.net/weixin_41577291/article/details/108691744
# 滑动窗口估计,发现数据变化趋势
from statsmodels.tsa.holtwinters import SimpleExpSmoothing


def plotMovingAverage(series, window, plot_intervals=False, scale=1.96, plot_anomalies=False):
    """
        series - dataframe with timeseries
        window - rolling window size
        plot_intervals - show confidence intervals
        plot_anomalies - show anomalies
    """
    rolling_mean = series.rolling(window=window).mean()
    plt.figure(figsize=(13, 5))
    plt.title("Moving average\n window size = {}".format(window))
    plt.plot(rolling_mean, "g", label="Rolling mean trend")
    # Plot confidence intervals for smoothed values
    if plot_intervals:
        mae = mean_absolute_error(series[window:], rolling_mean[window:])
        deviation = np.std(series[window:] - rolling_mean[window:])
        lower_bond = rolling_mean - (mae + scale * deviation)
        upper_bond = rolling_mean + (mae + scale * deviation)
        plt.plot(upper_bond, "r--", label="Upper Bond / Lower Bond")
        plt.plot(lower_bond, "r--")
        # Having the intervals, find abnormal values
        if plot_anomalies:
            anomalies = pd.DataFrame(index=series.index)
            anomalies['series<lower_bond'] = series[series < lower_bond]
            anomalies['series>upper_bond'] = series[series > upper_bond]
            plt.plot(anomalies, "ro", markersize=10)
    plt.plot(series[window:], label="Actual values")
    plt.legend(loc="upper left")
    plt.grid(True)
    # plt.show()


def exponential_smoothing(series, alpha):
    """
        series - dataset with timestamps
        alpha - float [0.0, 1.0], smoothing parameter
    """
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result


# 平滑结果显示图
def plotExponentialSmoothing(series, alphas):
    """
        Plots exponential smoothing with different alphas

        series - dataset with timestamps
        alphas - list of floats, smoothing parameters

    """
    with plt.style.context('classic'):
        plt.figure(figsize=(15, 7))
        for alpha in alphas:
            plt.plot(exponential_smoothing(series, alpha), label="Alpha {}".format(alpha))
        plt.plot(series.values, "c", label="Actual")
        plt.legend(loc="best")
        plt.axis('tight')
        plt.title("Exponential Smoothing")
        plt.grid(True)
        plt.show()


def single_exp_smoothing(df, length):
    alpha = 0.5
    df = pd.Series(np.squeeze(df.values))
    fit1 = SimpleExpSmoothing(df).fit(smoothing_level=alpha, optimized=False)
    fcast1 = fit1.forecast(length).rename('SES_Pred')
    fcast1 = fcast1.reset_index(drop=True)

    # fcast1.plot(marker='o', legend=True, figsize=(12, 4))
    # fit1.fittedvalues.plot()
    # print(fcast1)
    # plt.show()
    return fcast1


# data = pd.read_excel('09days_96p_price.xlsx', usecols=['data', 'price'])
# plotMovingAverage(data['price'], 12, plot_intervals=True, scale=1.96, plot_anomalies=True)
# plotExponentialSmoothing(data['price'], [0.5, 0.1])

