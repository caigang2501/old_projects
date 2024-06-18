# -*- coding: utf-8 -*-
#电能量市场用到的库
from mid_long.Medium_long_term_forecast import decom_price_test_pred_5, comxlsx_ml, XGBoost_5, GABPNet_5, Transformer_5
from mid_long.Medium_long_term_forecast import COM_Fore_Price as cfp

import pandas as pd
import os
######################################################################################
"""电能量市场"""
"""中长期预测"""
def main(pred_length,path_5):
    Transformer_5.transformer(path_5, length=pred_length)
    GABPNet_5.gabpnet(path_5, length=pred_length)
    XGBoost_5.xgboost(path_5, length=pred_length)
    decom_price_test_pred_5.run_model(path_5, length=pred_length)     # CEEMDAN + ARIMA 测试和预测输出

    test_5, predict_5 = comxlsx_ml.comxlsx(path_5, length=pred_length)
    fpoints_test, fpoints_pred = (os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/5_test.xlsx'),
                                  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'result/5_predict.xlsx'))
    (mid_long_fore, error_com) = cfp.com_fore_price(fpoints_test, fpoints_pred)
    df = pd.DataFrame(mid_long_fore)
    # workbook = openpyxl.Workbook()
    df.to_excel(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             'trading_strategy/bidding/5_com_pred.xlsx'), index=False)

    print("中长期竞价价格----组合预测价格(未来12个月电力交易价格预测): ", mid_long_fore)
    print("综合预测误差为:", error_com*100, '%')
    return mid_long_fore

######################################################################################

if __name__=='__main__':
    #年度集中竞价
    print("年度集中竞价平段电力交易价格预测结果")
    main(12,'history_50_220107_231110ping.xlsx')
    print("年度集中竞价峰段电力交易价格预测结果")
    main(12,'history_50_220107_231110gu.xlsx')
    print("年度集中竞价谷段电力交易价格预测结果")
    main(12,'history_50_220107_231110feng.xlsx')
    #月度集中竞价
    print("某月月度集中竞价平段电力交易价格预测结果")
    main(1,'history_50_220107_231110ping.xlsx')
    print("某月月度集中竞价峰段电力交易价格预测结果")
    main(1,'history_50_220107_231110gu.xlsx')
    print("某月月度集中竞价谷段电力交易价格预测结果")
    main(1,'history_50_220107_231110feng.xlsx')