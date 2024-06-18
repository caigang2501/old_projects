"""
调频竞价交易
"""
# import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
from service_marcket.guizhou.tiaoping import COM_Fore_Price
import os

def asfm96():  
    # Configuration
    fpoints_test, fpoints_pred = os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_test.xlsx'), os.path.join(os.path.dirname(os.path.abspath(__file__)),'result/asfm96_predict.xlsx')
    (asfm96,error_com)  = COM_Fore_Price.com_fore_price(fpoints_test, fpoints_pred)
    asfm96 = np.expand_dims(asfm96, axis=1)
    asfm96 = [sum(asfm96[i:i+4]) / 4 for i in range(0, len(asfm96), 4)]
    asfm96 = np.concatenate(asfm96)
    print("调频价格预测误差为:", error_com*100,'%')
    print("调频24时点报价为： ", asfm96)
    return asfm96























