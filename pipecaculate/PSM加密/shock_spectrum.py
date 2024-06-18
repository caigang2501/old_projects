import os.path
import pprint
import math


class ShockSpectrum:

    def __init__(self):
        pass

    def cal_shock(self, prd_path):
        """
        开始get prd文件冲击部分内容
        :param prd_path:
        :return:
        """
        total_mass = {}
        frequencys = {}
        num = 0
        num1 = 0
        mmx, mmy, mmz = '', '', ''
        with open(prd_path, 'r', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):

                if 'MODE=' in line and 'PERIOD=' in line and 'FREQUENCY=' in line and 'CONTINUED' not in line:
                    num1 = num1+1
                    frequencys[num1] = float(line.split()[5])

                if 'MODAL MASS (KG)' in line:
                    num = num + 1
                    mmx, mmy, mmz = float(line.split()[6]), float(line.split()[8]), float(line.split()[10])
                    total_mass[num] = {}
                    total_mass[num]['x'] = mmx
                    total_mass[num]['y'] = mmy
                    total_mass[num]['z'] = mmz

                if 'CUM MODAL MASS / TOTAL MASS' in line:

                    mmx, mmy, mmz = float(line.split()[7]), float(line.split()[9]), float(line.split()[11])

                    if mmx >= 0.8 and mmy >= 0.8 and mmz >= 0.8:
                        return total_mass, frequencys

    def cal_a_v(self, mass, frequency, dir_name, prd_name):
        """
        计算每一阶频率的A——v
        水面船体
        水面甲板
        潜艇船体
        潜艇甲板
        :param mass:mass
        :param f:frequency
        :return:
        """
        f_s1 = []
        f_s2 = []
        f_s3 = []
        f_s4 = []
        f_s5 = []
        f_s6 = []
        f_s7 = []
        f_s8 = []
        f_s9 = []
        f_s10 = []
        f_s11 = []
        f_s12 = []
        total_line = {}
        water_hull = ''
        water_deck = ''
        oscar_hull = ''
        oscar_deck = ''

        shock_path = os.path.join(dir_name, '%s_shock.txt' % prd_name)
        if os.path.exists(shock_path):
            os.remove(shock_path)

        with open(shock_path, 'a') as fn:

            for key in ['水面船体', '水面甲板', '潜艇船体', '潜艇甲板']:
                if key == '水面船体':
                    for m in mass.keys():
                        f = frequency[m]

                        x, y, z = mass[m]['x'], mass[m]['y'], mass[m]['z']
                        A0 = 196.2 * (17.01 + x) * (5.44 + x)/((2.72 + x)**2)
                        A1 = 196.2 * (17.01 + y) * (5.44 + y)/((2.72 + y)**2)
                        A2 = 196.2 * (17.01 + z) * (5.44 + z)/((2.72 + z)**2)
                        V0 = 1.52 * (5.44 + x)/(2.72 + x)
                        V1 = 1.52 * (5.44 + y)/(2.72 + y)
                        V2 = 1.52 * (5.44 + z)/(2.72 + z)
                        ax = 0.2 * A0
                        vx = 0.2 * V0
                        ay = 0.4 * A1
                        vy = 0.4 * V1
                        az = 1.0 * A2
                        vz = 1.0 * V2
                        speed_x = min(ax, 2 * math.pi * vx / f) / 9.81
                        speed_y = min(ay, 2 * math.pi * vy / f) / 9.81
                        speed_z = min(az, 2 * math.pi * vz / f) / 9.81
                        print(ax, vx, speed_x)
                        f2 = self.get_one_float(f)
                        x_round = '%s/%s' % (f2, round(speed_x, 3))
                        y_round = '%s/%s' % (f2, round(speed_y, 3))
                        z_round = '%s/%s' % (f2, round(speed_z, 3))
                        f_s1.append(x_round)
                        f_s2.append(y_round)
                        f_s3.append(z_round)

                elif key == '水面甲板':
                    for m in mass.keys():
                        f = frequency[m]
                        x, y, z = mass[m]['x'], mass[m]['y'], mass[m]['z']
                        A0 = 98.1 * (19.05 + x) / (2.72 + x)
                        V0 = 1.52 * (5.44 + x) / (2.72 + x)
                        A1 = 98.1 * (19.05 + y) / (2.72 + y)
                        V1 = 1.52 * (5.44 + y) / (2.72 + y)
                        A2 = 98.1 * (19.05 + z) / (2.72 + z)
                        V2 = 1.52 * (5.44 + z) / (2.72 + z)
                        ax = 0.2 * A0
                        vx = 0.2 * V0
                        ay = 0.4 * A1
                        vy = 0.2 * V1
                        az = 1.0 * A2
                        vz = 0.5 * V2

                        speed_x = min(ax, 2 * math.pi * vx / f) / 9.81
                        speed_y = min(ay, 2 * math.pi * vy / f) / 9.81
                        speed_z = min(az, 2 * math.pi * vz / f) / 9.81

                        f2 = self.get_one_float(f)
                        x_round = '%s/%s' % (f2, round(speed_x, 3))
                        y_round = '%s/%s' % (f2, round(speed_y, 3))
                        z_round = '%s/%s' % (f2, round(speed_z, 3))
                        f_s4.append(x_round)
                        f_s5.append(y_round)
                        f_s6.append(z_round)

                elif key == '潜艇船体':
                    for m in mass.keys():
                        f = frequency[m]
                        x, y, z = mass[m]['x'], mass[m]['y'], mass[m]['z']
                        A0 = 102.02 * (217.73 + x) / (9.07 + x)
                        V0 = 0.51 * (217.73 + x) / (45.36 + x)
                        A1 = 102.02 * (217.73 + y) / (9.07 + y)
                        V1 = 0.51 * (217.73 + y) / (45.36 + y)
                        A2 = 102.02 * (217.73 + z) / (9.07 + z)
                        V2 = 0.51 * (217.73 + z) / (45.36 + z)
                        ax = 0.4 * A0
                        vx = 0.4 * V0
                        ay = 1.0 * A1
                        vy = 1.0 * V1
                        az = 1.0 * A2
                        vz = 1.0 * V2

                        speed_x = min(ax, 2 * math.pi * vx / f) / 9.81
                        speed_y = min(ay, 2 * math.pi * vy / f) / 9.81
                        speed_z = min(az, 2 * math.pi * vz / f) / 9.81

                        f2 = self.get_one_float(f)
                        x_round = '%s/%s' % (f2, round(speed_x, 3))
                        y_round = '%s/%s' % (f2, round(speed_y, 3))
                        z_round = '%s/%s' % (f2, round(speed_z, 3))
                        f_s7.append(x_round)
                        f_s8.append(y_round)
                        f_s9.append(z_round)

                elif key == '潜艇甲板':
                    for m in mass.keys():
                        f = frequency[m]
                        x, y, z = mass[m]['x'], mass[m]['y'], mass[m]['z']
                        A0 = 102.02 * (217.73 + x) / (9.07 + x)
                        V0 = 0.51 * (217.73 + x) / (45.36 + x)
                        A1 = 102.02 * (217.73 + y) / (9.07 + y)
                        V1 = 0.51 * (217.73 + y) / (45.36 + y)
                        A2 = 102.02 * (217.73 + z) / (9.07 + z)
                        V2 = 0.51 * (217.73 + z) / (45.36 + z)
                        ax = 0.4 * A0
                        vx = 0.4 * V0
                        ay = 1.0 * A1
                        vy = 1.0 * V1
                        az = 0.5 * A2
                        vz = 0.5 * V2

                        speed_x = min(ax, 2 * math.pi * vx / f) / 9.81
                        speed_y = min(ay, 2 * math.pi * vy / f) / 9.81
                        speed_z = min(az, 2 * math.pi * vz / f) / 9.81

                        f2 = self.get_one_float(f)
                        x_round = '%s/%s' % (f2, round(speed_x, 3))
                        y_round = '%s/%s' % (f2, round(speed_y, 3))
                        z_round = '%s/%s' % (f2, round(speed_z, 3))
                        f_s10.append(x_round)
                        f_s11.append(y_round)
                        f_s12.append(z_round)
            flag1 = '  ******水面船体*********************' + 2*'\n'
            fn.write(flag1)
            res = self.make_average_list(f_s1, 5)
            t1 = self.make_f_s_line('DI=X', res)
            fn.write(t1)
            res = self.make_average_list(f_s2, 5)
            t2 = self.make_f_s_line('DI=Y', res)
            fn.write(t2)
            res = self.make_average_list(f_s3, 5)
            t3 = self.make_f_s_line('DI=Z', res)
            fn.write(t3)
            fn.write('\n')
            water_hull += 2*'\n' + flag1 + t1 + t2 + t3
            total_line['水面船体'] = water_hull

            flag2 = '  ******水面甲板*********************' + 2*'\n'
            fn.write(flag2)
            res = self.make_average_list(f_s4, 5)
            t4 = self.make_f_s_line('DI=X', res)
            fn.write(t4)
            res = self.make_average_list(f_s5, 5)
            t5 = self.make_f_s_line('DI=Y', res)
            fn.write(t5)
            res = self.make_average_list(f_s6, 5)
            t6 = self.make_f_s_line('DI=Z', res)
            fn.write(t6)
            fn.write('\n')
            water_deck = 2*'\n' + flag2+ t4 + t5 + t6
            total_line['水面甲板'] = water_deck

            flag3 = '  ******潜艇船体*********************' + 2*'\n'
            fn.write(flag3)
            res = self.make_average_list(f_s7, 5)
            t7 = self.make_f_s_line('DI=X', res)
            fn.write(t7)
            res = self.make_average_list(f_s8, 5)
            t8 = self.make_f_s_line('DI=Y', res)
            fn.write(t8)
            res = self.make_average_list(f_s9, 5)
            t9 = self.make_f_s_line('DI=Z', res)
            fn.write(t9)
            fn.write('\n')
            oscar_hull = 2*'\n' + flag3 + t7 + t8 + t9
            total_line['潜艇船体'] = oscar_hull

            flag4 = '  ******潜艇甲板*********************' + 2*'\n'
            fn.write(flag4)
            res = self.make_average_list(f_s10, 5)
            t10 = self.make_f_s_line('DI=X', res)
            fn.write(t10)
            res = self.make_average_list(f_s11, 5)
            t11 = self.make_f_s_line('DI=Y', res)
            fn.write(t11)
            res = self.make_average_list(f_s12, 5)
            t12 = self.make_f_s_line('DI=Z', res)
            fn.write(t12)
            fn.write('\n')
            oscar_deck = 2*'\n' + flag4 + t10 + t11 + t12
            total_line['潜艇甲板'] = oscar_deck

        return shock_path, total_line

    @staticmethod
    def get_one_float(f_str):
        """
        圆整到一个数字
        :param f_str:
        :return:
        """

        f_str = str(f_str)
        if '.' in f_str:
            a, b, c = f_str.partition(".")
            c = c[0]
            return '.'.join([a, c])
        else:
            return f_str

    @staticmethod
    def make_average_list(ls, size):
        """
        均分列表
        :param size: 个数
        :return:
        """
        return [ls[i:i+size] for i in range(0, len(ls), size)]

    @staticmethod
    def make_f_s_line(titile, ls):
        """
        制作行数
        :param ls: 数据列表频率和加速度
        :return: 要写入的数据行
        """
        t = '       ' + titile+'\n'
        for l in ls:
            t += '         ' + ' '.join(l) + '\n'

        return t



