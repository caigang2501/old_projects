"""
调频竞价交易
"""
from service_marcket.ganshu import COM_Fore_Price
import numpy as np
import os
def midlong(marginal_unit):  
    # Configuration
    fpoints_test, fpoints_pred = os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_test.xlsx'), os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm_predict.xlsx')
    (fm_fore,error_com)  = COM_Fore_Price.com_fore_price(fpoints_test, fpoints_pred)
    six = np.average(fm_fore)
    fm_fore = np.append(fm_fore, six)
    print("调频竞价价格----组合预测价格: ", fm_fore)
    # print("调频价格预测误差为:", error_com*100,'%')          
    # 调频里程成本（元/MW）
    per_cost = 5
    
    if marginal_unit:
        print("调频里程竞价报价：", fm_fore)
    else:
        print("调频里程竞价该日统一报价：", per_cost)
    return fm_fore






















