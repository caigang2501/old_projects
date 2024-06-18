"""
中长期双边协商
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def main(path):
    data_df = pd.read_excel(path, sheet_name='DATA', header=0)
    (N, p1, limit1, p2, limit2, k1, k2) = data_df.iloc[0]

    # 购电方的贴现因子
    def discount1(offers1, offers2, n):
        if len(offers1) < 3:
            return (n / N) **k2
        else:
            return (n / N) ** (k2*(offers1[-1] / p1 + offers2[-1] / offers2[-2]))


    # 售电方的贴现因子
    def discount2(offers1, offers2, n):
        if len(offers2) < 3:
            return (n / N) ** k1
        else:
            return (n / N) ** (k1*(p2 / offers2[-1] + offers1[-2] / offers1[-1]))


    # 购电方的报价函数
    def offer1(offers1, offers2, n):
        if len(offers1) == 0:
            return p1
        else:
            return offers1[-1] + discount1(offers1, offers2, n) * (limit1 - offers1[-1])

    # 售电方的报价函数


    def offer2(offers1, offers2, n):
        if len(offers2) == 0:
            return p2
        else:
            return offers2[-1] - discount2(offers1, offers2, n) * (offers2[-1]-limit2)


    # 初始化报价列表
    offers1 = []
    offers2 = []

    # 进行鲁宾斯轮流讨价还价博弈
    for i in range(N):
        if i % 2 == 0:
            offers1.append(offer1(offers1, offers2, i))
            offers2.append(offer2(offers1, offers2, i))
        else:
            offers2.append(offer2(offers1, offers2, i))
            offers1.append(offer1(offers1, offers2, i))

    # 求距离两条曲线交点最近的点
    offers1 = np.array(offers1)
    offers2 = np.array(offers2)
    minus = np.abs(offers1 - offers2)
    n = np.argmin(minus)

    # 输出最终成交价格
    # 下面print打开会导致bug，测试完请关闭
    # print("建议最终成交价格为:", (offers1[n] + offers2[n]) / 2)

    # 输出报价折线图
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['font.sans-serif'] = ['SimSun']
    plt.plot(np.arange(1, N+1), offers1, label='购电商',
             marker='s', linewidth=1, markersize=0.5)
    plt.plot(np.arange(1, N+1), offers2, label='售电商',
             marker='s', linewidth=1, markersize=0.5)
    # plt.scatter(np.arange(1, N+1), offers1, s=5,marker='s')
    # plt.scatter(np.arange(1, N+1), offers2, s=5,marker='s')
    plt.legend()
    plt.xlim(1, 20)
    plt.xlabel('报价轮次')
    plt.ylabel('电力价格（yuan/MWh）')
    plt.yticks(fontproperties='Times New Roman')
    plt.xticks(np.linspace(1, 20, 20, endpoint=True),
               fontproperties='Times New Roman')
    # plt.show()
    return (offers1[n] + offers2[n]) / 2

if __name__=='__main__':
    main('input_data.xlsx')