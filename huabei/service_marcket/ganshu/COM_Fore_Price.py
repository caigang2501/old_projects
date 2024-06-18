"""
甘肃调频市场
"""
import pandas as pd
# import math
import numpy as np


def com_fore_price(test_res_path, pred_res_path):     # 测试结果保存路径
    pf1 = pd.read_excel(test_res_path)     # pf = [预测点数, 真实值 + 预测值 * 6]
    pf2 = pd.read_excel(pred_res_path)     # pf = [预测点数, 预测值 * 6]

    # 综合误差值
    def comp_err(actual, pred):  # actual = pred = [n, ]
        N = len(pred)
        # sum_rmse = 0.0
        sum_mape = 0.0
        for i in range(N):
        #    sum_rmse += (actual[i] - pred[i]) ** 2
            sum_mape += abs((actual[i] - pred[i]) / actual[i])

        #rmse_val = math.sqrt(sum_rmse / N)  # 均方根误差----RMSE, Root Mean Squared Error
        mape_val = sum_mape / N  # 平均绝对百分比误差----MAPE, Mean Absolute Percentage Error
        compree_val =mape_val# (rmse_val + mape_val) / 2

        return compree_val

    # 权重计算
    def weight_val(compree_model):  # compree_model = [6, 1]
        sum = 0.0
        weight = []
        for i in range(0, 6):
            sum += 1.0 / compree_model[i]
        for i in range(0, 6):
            weig = (1.0 / compree_model[i]) / sum
            weight.append(weig)
        weight = np.array(weight)

        return weight

    # 最终预测价格
    def weighted_price(pred_price, weight):  # pred_price = [96 / 5, 6], weight = [6, 1]
        final = pred_price[:, 0] * weight[0]
        for i in range(1, 6):
            pr = pred_price[:, i] * weight[i]
            final = np.vstack((final, pr))  # final = [6, 96 / 5]
        final_price = np.sum(final, axis=0)

        return final_price  # final_price = [1, 96 / 5]

    error = []
    for i in range(1, 7):
        error.append(comp_err(pf1.iloc[:, 0], pf1.iloc[:, i]))
    weights =np.array([0.,0.,0.,0.,0.23,0.]) # weight_val(np.array(error))
    error_com = np.sum(error * weights)
    weights1 =np.array([0,0,0,0,1,0])
    predict = pf2.values
    price = weighted_price(predict, weights1)

 #   weights = weight_val(np.array(error))
 #   predict = pf2.values
 #   price = weighted_price(predict, weights)
 #   error_com = np.sum(error * weights)
    return price,error_com


# fpoints_test, fpoints_pred, npoints_test, npoints_pred = '5_test.xlsx', '5_predict.xlsx', '96_test.xlsx', '96_predict.xlsx'

# print("中长期竞价价格----组合预测价格: ", com_fore_price(fpoints_test, fpoints_pred))
# print("现货日前价格-----组合预测价格: ", com_fore_price(npoints_test, npoints_pred))




