"""
现货报价
"""

import numpy as np
import pandas as pd
import warnings
import os
warnings.filterwarnings(action='ignore')


def spot(path, marginal_unit):
    df = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'机组成本.xlsx'), header=None)
    # npoints_test, npoints_pred = './result/96_test.xlsx', './result/96_predict.xlsx'
    # day_ahead_fore = COM_Fore_Price.com_fore_price(npoints_test, npoints_pred)
    day_ahead_fore = pd.read_excel(path, header=None)
    # day_ahead_fore = np.expand_dims(day_ahead_fore, axis=1)
    # print("现货日前价格-----组合预测价格: ", day_ahead_fore)
    
    # 机组成本----数据集----后续可改为文件调用
    # unit_id = np.array([1, 2, 3])     # 机组ID：1----photovoltaic; 2----wind_power; 3----thermal_power
    # unit_type = ['photovoltaic', 'wind_power', 'thermal_power']    # 机组类型
    # minimum_output = np.array([0, 150, 700])     # 机组最小技术出力
    # minimum_output = np.array(df.iloc[1:, 2])     # 机组最小技术出力 (3, )
    # rated_power = np.array([300, 300, 2000])     # 机组额定功率
    # rated_power = np.array(df.iloc[1:, 3])     # 机组额定功率 (3, )

    # 能源基地最大最小出力
    # enba_output_min = np.sum(minimum_output)     # 能源基地最大出力 ----> 850
    # enba_output_max = np.sum(rated_power)     # 能源基地最小出力 ----> 2600
    
    # 各机组类型度电成本 ----> 光伏, 风电, 燃煤
    # unit_per_cost = np.array([350, 360, 345])
    
    # 第一段 ----> 第十段起始出力; initial_output = [3, 11]
    """initial_output = np.array([[0, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300],
                               [150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300],
                               [700, 830, 960, 1090, 1220, 1350, 1480, 1610, 1740, 1870, 2000]
                               ])"""
    initial_output = np.array(df.loc[1:, 4: 14])
    # 第一段 ----> 第十段度电成本; cost_per = [3, 10]
    """cost_per = np.array([[180, 200, 210, 220, 240, 250, 270, 280, 290, 300],
                         [180, 200, 210, 220, 240, 250, 270, 280, 290, 300],
                         [270, 270, 280, 280, 280, 290, 290, 290, 290, 300]
                         ])"""
    cost_per = np.array(df.loc[1:, 15: 24])
    
    # 能源基地预测的96时段各机组出力
    unit_forecast_output = pd.read_excel(os.path.join(os.path.dirname(os.path.abspath(__file__)),'unit_forecast_output.xlsx'), usecols=['period_forecast_output'])
    photo_fore_output = np.array(unit_forecast_output.iloc[0:96])     # photo_fore_output = [96, 1]
    wind_fore_output = np.array(unit_forecast_output.iloc[96:96*2])     # wind_fore_output = [96, 1]
    thermal_fore_output = np.array(unit_forecast_output.iloc[96*2:])     # thermal_fore_output = [96, 1]
    
    # 能源基地预测的96时段出力
    unit_fore_output = photo_fore_output + wind_fore_output + thermal_fore_output     # [96, 1]
    
    # 能源基地预测的96时段各类型机组出力比例
    unit_sum = np.concatenate((photo_fore_output, wind_fore_output, thermal_fore_output), axis=1)     # [96, 3]
    unit = np.sum(unit_sum, axis=0)
    unit_ratio = (unit / np.sum(unit_sum)).reshape((1, 3))      # [1, 3]
    unit_ratio = np.tile(unit_ratio, (10, 1))

    # 出力与成本匹配函数
    def output_match_cost(unit_id, unit_output):
        cost = []
        for i in range(10):
            if (unit_id == 1 and unit_output < initial_output[0, 0]) \
                    or (unit_id == 2 and unit_output < initial_output[1, 0]) \
                    or (unit_id == 3 and unit_output < initial_output[2, 0]):
                cost = 0
            if initial_output[unit_id - 1, i] <= unit_output <= initial_output[unit_id - 1, i + 1]:
                cost = cost_per[unit_id - 1, i]
    
        return cost

    # 能源基地预测的96时段各机组类型出力成本
    photo_fore_cost = []
    wind_fore_cost = []
    thermal_fore_cost = []
    for i in range(96):
        photo_fore_cost.append(output_match_cost(1, photo_fore_output[i]))
        wind_fore_cost.append(output_match_cost(2, wind_fore_output[i]))
        thermal_fore_cost.append(output_match_cost(3, thermal_fore_output[i]))
    
    photo_fore_cost = np.array(photo_fore_cost).reshape((96, 1))  # [96, 1]
    wind_fore_cost = np.array(wind_fore_cost).reshape((96, 1))  # [96, 1]
    thermal_fore_cost = np.array(thermal_fore_cost).reshape((96, 1))  # [96, 1]
    photo_fore_output = np.array(photo_fore_output)  # [96, 1]
    wind_fore_output = np.array(wind_fore_output)
    thermal_fore_output = np.array(thermal_fore_output)
    # 能源基地预测的96时段出力成本
    pred_output_cost = photo_fore_cost * photo_fore_output + wind_fore_cost * wind_fore_output + thermal_fore_cost * thermal_fore_output#这里加的错了，现在加的是度电成本，应该是总成本，即度电成本*出力
    #pred_output_cost = np.array(pred_output_cost)
    #pred_output_cost = np.expand_dims(pred_output_cost, axis=1)  # [96, 1]
    
    # 新能源基地预测的96时段出力度电成本
    fore_cost_per = []
    for i in range(96):
        fore_cost_per.append(pred_output_cost[i] / unit_fore_output[i])
    fore_cost_per = np.array(fore_cost_per)  # [96, 1]

    num = np.zeros(10)  # 各出力段预测值的数目 ----> [0.  0.  0.  0.  0. 23. 13. 36. 17.  7.]
    mark = np.zeros((96, 1))

    min_output = np.sum(initial_output[:, 0])
    max_output = np.sum(initial_output[:, -1])
    interval = int((max_output - min_output) / 10)
    output_total = np.arange(1, 11)

    matrix = np.hstack([mark, unit_fore_output, day_ahead_fore, fore_cost_per])
    # mark标识, 96时段出力, 预测价格, 时段度电成本 ----> [96, 4]
    for i in range(96):
        for j in range(0, 10):
            output_total[j] = min_output + interval * j
            if min_output + interval * j <= matrix[i, 1] <= min_output + interval * (j + 1):
                matrix[i, 0] = j
                num[j] += 1
    output_total = np.append(output_total, max_output)
    # 未筛选出出力段的报价
    no_part = []
    for i in range(10):
        no_part.append(min_output + interval/2*(i+1))     # unit_ratio = [0.03500237, 0.12253484, 0.84246279]
    no_part = np.array(no_part).reshape((10, 1))
    no_part = np.tile(no_part, (1, 3))
    part_one = unit_ratio * no_part
    photo_fore_cost_no = []
    wind_fore_cost_no = []
    thermal_fore_cost_no = []
    
    for i in range(10):
        photo_fore_cost_no.append(output_match_cost(1, part_one[i, 0]))
        wind_fore_cost_no.append(output_match_cost(2, part_one[i, 1]))
        thermal_fore_cost_no.append(output_match_cost(3, part_one[i, 2]))
    photo_fore_cost_no = np.array(photo_fore_cost_no).reshape((10, 1))
    wind_fore_cost_no = np.array(wind_fore_cost_no).reshape((10, 1))
    thermal_fore_cost_no = np.array(thermal_fore_cost_no).reshape((10, 1))
    
    photo_fore_cost_no = np.nan_to_num(np.asarray(photo_fore_cost_no, dtype=float))
    wind_fore_cost_no = np.nan_to_num(np.asarray(wind_fore_cost_no, dtype=float))
    thermal_fore_cost_no = np.nan_to_num(np.asarray(thermal_fore_cost_no, dtype=float))
    imm = np.concatenate((photo_fore_cost_no, wind_fore_cost_no, thermal_fore_cost_no), axis=1)
    no_part_total = []
    no_part_total = np.sum(imm * unit_ratio, axis=1)
    no_part_total = np.array(no_part_total).reshape(10, 1)
    # 能源基地十个出力段的各出力段报价     # mark标识, 96时段出力, 预测价格, 时段度电成本 ----> [96, 4]
    spot_quotation0 = np.zeros(10)
    spot_quotation1 = np.zeros(10)
    for i in range(10):
        _tmp = []
        if num[i] == 0:
            spot_quotation0[i] = no_part_total[i]
            spot_quotation1[i] = no_part_total[i]
        if num[i] != 0:
            for j in range(96):
                if matrix[j, 0] == i:
                    _tmp.append(matrix[j, :])
            _tmp = np.array(_tmp)
            spot_quotation0[i] = np.sum((_tmp[:, 1] / np.sum(_tmp[:, 1])) * _tmp[:, 3])
            _tmp = []
            for j in range(96):
                if matrix[j, 0] == i:
                    _tmp.append(matrix[j, :])
            _tmp = np.array(_tmp)
            spot_quotation1[i] = np.sum((_tmp[:, 1] / np.sum(_tmp[:, 1])) * _tmp[:, 2])
    print(output_total)
    print("现货日前报价：", spot_quotation0,spot_quotation1)
    spot_quotation00 = [spot_quotation0[0]]
    spot_quotation11 = [spot_quotation1[0]]
    # 确保数据单调不递减
    for i in range(1, len(spot_quotation0)):
        if spot_quotation0[i] < spot_quotation00[-1]:
            spot_quotation00.append(spot_quotation00[-1])
        else:
            spot_quotation00.append(spot_quotation0[i])
    print("现货日前报价单调不递减：", spot_quotation00)
    for i in range(1, len(spot_quotation1)):
        if spot_quotation1[i] < spot_quotation11[-1]:
            spot_quotation11.append(spot_quotation11[-1])
        else:
            spot_quotation11.append(spot_quotation1[i])
    print("现货日前报价单调不递减：", spot_quotation11)
    return spot_quotation0,spot_quotation1,spot_quotation00,spot_quotation11,

if __name__=='__main__':
    predict_result = os.path.join(os.path.dirname(os.path.abspath(__file__)),'final_predict.xlsx')
    spot(predict_result, marginal_unit=0)
    result = spot(predict_result)
    print(result['range'])
    print("现货日前报价：", result['noseek'],result['seek'])



