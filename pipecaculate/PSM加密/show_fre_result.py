import os
from PyQt5.QtWidgets import QMessageBox, QMainWindow


class GetMaxResult(QMainWindow):
    def __init__(self, dir_path, max_filename_list, max_path):
        super().__init__()
        self.dir_path = dir_path
        self.max_filename_list = max_filename_list
        self.old_max_path = max_path

    def get_max_files(self):
        """
        获取.max所在文件路径
        :return:
        """
        fre_less1 = []
        eq8_all = []
        eq_ab9_all = []
        eq_ab10_all = []
        eq_ab11_all = []
        eq_c9_all = []
        eq_d9_all = []
        eq_water_all = []
        data_dict = {'O级准则-方程8': '', 'AB级准则-方程9': '', 'AB级准则 方程10': '', 'AB级准则 方程11': '',
                     'C级准则 方程9': '', 'D级准则 方程9': '', '水压试验': ''}
        # 应力比小于1的优化工况字典数据
        data_dict2 = {}
        # m1, m2, m3, m4, m5, m6, m7 = [], [], [], [], [], [], []
        try:
            # 读取原来得max文件，获取结果
            if os.path.exists(self.old_max_path):
                name = os.path.basename(self.old_max_path)
                file_name = os.path.splitext(name)[0]
                eq8, eq_ab9, eq_ab10, eq_ab11, eq_c9, eq_d9, eq_water = self.deal_max_table(self.old_max_path, file_name)
                if eq8:
                    eq8_all.append(eq8)
                if eq_ab9:
                    eq_ab9_all.append(eq_ab9)
                if eq_ab10:
                    eq_ab10_all.append(eq_ab10)
                if eq_ab11:
                    eq_ab11_all.append(eq_ab11)
                if eq_c9:
                    eq_c9_all.append(eq_c9)
                if eq_d9:
                    eq_d9_all.append(eq_d9)
                if eq_water:
                    eq_water_all.append(eq_water)

            if self.max_filename_list:
                for m in self.max_filename_list:
                    t1, t2, t3, t4, t5, t6, t7 = False, False, False, False, False, False, False
                    eq8_less1, eq_ab9_less1, eq_ab10_less1, eq_ab11_less1, eq_c9_less1, eq_d9_less1, eq_water_less1 = [], [], [], [], [], [], []
                    max_result_path = os.path.join(self.dir_path, m)

                    print(max_result_path, "ddddddddd")

                    name = os.path.basename(max_result_path)
                    file_name = os.path.splitext(name)[0]
                    less1_data = []
                    if os.path.exists(max_result_path):

                        eq8, eq_ab9, eq_ab10, eq_ab11, eq_c9, eq_d9, eq_water = self.deal_max_table(max_result_path, file_name)

                        if eq8:
                            eq8_all.append(eq8)
                            if float(eq8[-1]) < 1:
                                eq8_less1 = eq8.copy()

                                t1 = True
                        if eq_ab9:
                            eq_ab9_all.append(eq_ab9)
                            if float(eq_ab9[-1]) < 1:
                                eq_ab9_less1 = eq_ab9.copy()

                                t2 = True
                        if eq_ab10:
                            eq_ab10_all.append(eq_ab10)
                            if float(eq_ab10[-1]) < 1:
                                eq_ab10_less1 = eq_ab10.copy()

                                t3 = True
                        if eq_ab11:
                            eq_ab11_all.append(eq_ab11)
                            if float(eq_ab11[-1]) < 1:
                                eq_ab11_less1 = eq_ab11.copy()

                                t4 = True
                        if eq_c9:
                            eq_c9_all.append(eq_c9)
                            if float(eq_c9[-1]) < 1:
                                eq_c9_less1 = eq_c9.copy()

                                t5 = True
                        if eq_d9:
                            eq_d9_all.append(eq_d9)
                            if float(eq_d9[-1]) < 1:
                                eq_d9_less1 = eq_d9.copy()

                                t6 = True
                        if eq_water:
                            eq_water_all.append(eq_water)
                            if float(eq_water[-1]) < 1:
                                eq_water_less1 = eq_water.copy()

                                t7 = True
                    if t1 and t2 and t3 and t4 and t5 and t6 and t7:
                        del eq8_less1[0]
                        del eq_ab9_less1[0]
                        del eq_ab10_less1[0]
                        del eq_ab11_less1[0]
                        del eq_c9_less1[0]
                        del eq_d9_less1[0]
                        del eq_water_less1[0]
                        # eq8_less1.insert(0, "O级准则-方程8")
                        # eq_ab9_less1.insert(0, "AB级准则-方程9")
                        # eq_ab10_less1.insert(0, "AB级准则 方程10")
                        # eq_ab11_less1.insert(0, "AB级准则 方程11")
                        # eq_c9_less1.insert(0, "C级准则 方程9")
                        # eq_d9_less1.insert(0, "D级准则 方程9")
                        # eq_water_less1.insert(0, "水压试验")
                        eq8_less1.insert(0, "O-equation8")
                        eq_ab9_less1.insert(0, "AB-equation9")
                        eq_ab10_less1.insert(0, "AB-equation10")
                        eq_ab11_less1.insert(0, "AB-equation11")
                        eq_c9_less1.insert(0, "C-equation9")
                        eq_d9_less1.insert(0, "D-equation9")
                        eq_water_less1.insert(0, "Water_pressure")
                        less1_data.extend([eq8_less1, eq_ab9_less1, eq_ab10_less1, eq_ab11_less1, eq_c9_less1,
                                           eq_d9_less1, eq_water_less1])

                        file_name = file_name + '.fre'

                        file_name0 = os.path.splitext(name)[0]
                        fre_less1.append(file_name0)

                        title_less1 = ['EQUATION', 'AT', 'STRESS']
                        title_less2 = ['        ', '  ', 'RATIO ']
                        # title_less1 = ['EQUATION', 'AT', 'COMPUTED', 'ALLOWABLE', 'STRESS']
                        # title_less2 = ['        ', '  ', 'STRESS  ', 'STRESS   ', 'RATIO ']

                        line_data = self.deal_line_data(less1_data)

                        title_less = self.align_data(title_less1)
                        title0 = self.align_data(title_less2)
                        less1_title = '\n'*2 + file_name0 + '\n'*2 + title_less + title0 + '\n' + line_data

                        data_dict2[file_name0] = less1_title

                eq8_all.sort(key=lambda x: x[-1])
                eq_ab9_all.sort(key=lambda x: x[-1])
                eq_ab10_all.sort(key=lambda x: x[-1])
                eq_ab11_all.sort(key=lambda x: x[-1])
                eq_c9_all.sort(key=lambda x: x[-1])
                eq_d9_all.sort(key=lambda x: x[-1])
                eq_water_all.sort(key=lambda x: x[-1])

                title1 = '\n'*2 + 'LOADING CASE NO. 108     COMBINATION ANALYSIS - DESIGN CONDITION EQ.8' + '\n'*3
                title2 = '\n'*2 + 'LOADING CASE NO. 109     COMB.STRESS ANALYSIS - EQ.9 AB' + '\n'*3
                title4 = '\n'*2 + 'LOADING CASE NO. 110     COMBINATION ANALYSIS - MAX-THERMAL-AB EQ.10-AB' + '\n'*3
                title3 = '\n'*2 + 'LOADING CASE NO. 111     COMB.STRESS ANALYSIS - EQ.11-AB' + '\n'*3
                title5 = '\n'*2 + 'LOADING CASE NO. 140     COMB.STRESS ANALYSIS - EQ.9-C ' + '\n'*3
                title6 = '\n'*2 + 'LOADING CASE NO. 150     COMB.STRESS ANALYSIS - EQ.9-D' + '\n'*3
                title7 = '\n'*2 + 'LOADING CASE NO16     TEST WEIGHT ANALYSIS - HYDROTEST EQ.9-TEST' + '\n'*3

                # title = ['FILENAME', 'AT', 'COMPUTED', 'ALLOWABLE', 'STRESS']
                # title0 = ['        ', '  ', 'STRESS  ', 'STRESS   ', 'RATIO ']

                title = ['FILENAME', 'AT', 'STRESS']
                title0 = ['        ', '  ', 'RATIO ']

                title = self.align_data(title)
                title0 = self.align_data(title0)
                table_title = title + title0

                data_dict['O级准则-方程8'] = self.deal_line_data(eq8_all)
                data_dict['O级准则-方程8'] = title1 + '\n' + table_title + '\n' + data_dict['O级准则-方程8']

                data_dict['AB级准则-方程9'] = self.deal_line_data(eq_ab9_all)
                data_dict['AB级准则-方程9'] = title2 + '\n' + table_title + '\n' + data_dict['AB级准则-方程9']

                data_dict['AB级准则 方程10'] = self.deal_line_data(eq_ab10_all)
                data_dict['AB级准则 方程10'] = title4 + '\n' + table_title + '\n' + data_dict['AB级准则 方程10']

                data_dict['AB级准则 方程11'] = self.deal_line_data(eq_ab11_all)
                data_dict['AB级准则 方程11'] = title3 + '\n' + table_title + '\n' + data_dict['AB级准则 方程11']

                data_dict['C级准则 方程9'] = self.deal_line_data(eq_c9_all)
                data_dict['C级准则 方程9'] = title5 + '\n' + table_title + '\n' + data_dict['C级准则 方程9']

                data_dict['D级准则 方程9'] = self.deal_line_data(eq_d9_all)
                data_dict['D级准则 方程9'] = title6 + '\n' + table_title + '\n' + data_dict['D级准则 方程9']

                data_dict['水压试验'] = self.deal_line_data(eq_water_all)
                data_dict['水压试验'] = title7 + '\n' + table_title + '\n' + data_dict['水压试验']

                return data_dict, fre_less1, data_dict2
            else:

                QMessageBox.information(self, '提示', '文件夹里没有.max文件，或文件没内容')

        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', '文件夹里没有.max文件，或文件没内容')

    def deal_line_data(self, data):
        # 整理行，给行排序
        data_line = ''
        for item in data:
            data_line += self.align_data(item[:-1])
        return data_line

    @staticmethod
    def align_data(data):
        """
        对齐字符串，排序
        :param data: 数据
        :return:
        """
        data_line = ''
        for i, item in enumerate(data):
            if i == 0:
                data_line += item.ljust(30, ' ')
            else:
                data_line += item.ljust(13, ' ')
        data_line = data_line + '\n' + '\n'
        return data_line

    def deal_max_table(self, file_path, m):

        eq8 = []
        eq_ab9 = []
        eq_ab10 = []
        eq_ab11 = []
        eq_c9 = []
        eq_d9 = []
        eq_water = []

        with open(file_path, 'r') as f:
            while True:
                line = f.readline().strip('\n')

                if "LOADING CASE NO. 108" in line:
                    try:
                        eq8.append(m)
                        # eq8.append("O级准则-方程8")
                        for i in range(13):
                            line = f.readline()

                        line = f.readline()

                        # 节点，计算应力，许用应力，应力比值
                        # eq8.append(line.strip())
                        data2, data11, data13, data14 = self.analysis_line(line)
                        value1 = float(data11) + float(data13)
                        value2 = float(data14)
                        value3 = format(value1/value2, '.2f')
                        eq8.append(data2)
                        # eq8.append(format(value1, '.2f'))
                        # eq8.append(value3)
                        eq8.append(data14)
                        eq8.append(float(data14))
                    except Exception as e:
                        print(e)
                        eq8 = []

                if "LOADING CASE NO. 110" in line:
                    try:
                        eq_ab10.append(m)
                        # eq_ab10.append("AB级准则 方程10")

                        for i in range(15):
                            line = f.readline()

                        line = f.readline()

                        # eq_ab10.append(line.strip())

                        data2, data11, data12, data13 = self.analysis_line2(line)
                        value1 = float(data11) + float(data12)
                        value2 = float(data13)
                        value3 = format(value1 / value2, '.2f')
                        eq_ab10.append(data2)
                        # eq_ab10.append(format(value1, '.2f'))
                        # eq_ab10.append(value3)
                        eq_ab10.append(data13)
                        eq_ab10.append(float(data13))
                    except Exception as e:
                        print(e)
                        eq_ab10 = []

                if "LOADING CASE NO. 111" in line:
                    try:
                        eq_ab11.append(m)
                        # eq_ab11.append("AB级准则 方程11")

                        for i in range(13):
                            line = f.readline()

                        line = f.readline()

                        # eq_ab11.append(line.strip())
                        data2, data11, data12, data13 = self.analysis_line2(line)
                        value1 = float(data11) + float(data12)
                        value2 = float(data13)
                        value3 = format(value1 / value2, '.2f')
                        eq_ab11.append(data2)
                        # eq_ab11.append(format(value1, '.2f'))
                        # eq_ab11.append(value3)
                        eq_ab11.append(data13)
                        eq_ab11.append(float(data13))
                    except Exception as e:
                        print(e)
                        eq_ab11 = []

                if "LOADING CASE NO. 109" in line:
                    try:
                        eq_ab9.append(m)
                        # eq_ab9.append("AB级准则-方程9")

                        for i in range(13):
                            line = f.readline()

                        line = f.readline()

                        # eq_ab9.append(line.strip())

                        data2, data11, data13, data14 = self.analysis_line(line)
                        value1 = float(data11) + float(data13)
                        value2 = float(data14)
                        value3 = format(value1 / value2, '.2f')
                        eq_ab9.append(data2)
                        # eq_ab9.append(format(value1, '.2f'))
                        # eq_ab9.append(value3)
                        eq_ab9.append(data14)
                        eq_ab9.append(float(data14))
                    except Exception as e:
                        print(e)
                        eq_ab9 = []

                if "LOADING CASE NO. 140" in line:
                    try:
                        eq_c9.append(m)
                        # eq_c9.append("C级准则 方程9")

                        for i in range(13):
                            line = f.readline()

                        line = f.readline()

                        # eq_c9.append(line.strip())
                        data2, data11, data13, data14 = self.analysis_line(line)
                        value1 = float(data11) + float(data13)
                        value2 = float(data14)
                        value3 = format(value1 / value2, '.2f')
                        eq_c9.append(data2)
                        # eq_c9.append(format(value1, '.2f'))
                        # eq_c9.append(value3)
                        eq_c9.append(data14)
                        eq_c9.append(float(data14))
                    except Exception as e:
                        print(e)
                        eq_c9 = []

                if "LOADING CASE NO. 150" in line:
                    try:
                        eq_d9.append(m)
                        # eq_d9.append("D级准则 方程9")

                        for i in range(13):
                            line = f.readline()

                        line = f.readline()

                        is_write_info = False
                        # eq_d9.append(line.strip())
                        data2, data11, data13, data14 = self.analysis_line(line)
                        value1 = float(data11) + float(data13)
                        value2 = float(data14)
                        value3 = format(value1 / value2, '.2f')
                        eq_d9.append(data2)
                        # eq_d9.append(format(value1, '.2f'))
                        # eq_d9.append(value3)
                        eq_d9.append(data14)

                        eq_d9.append(float(data14))
                    except Exception as e:
                        print(e)
                        eq_d9 = []

                if "LOADING CASE NO.  16" in line:
                    try:
                        eq_water.append(m)
                        # eq_water.append("水压试验")

                        for i in range(11):
                            line = f.readline()

                        line = f.readline()

                        # eq_water.append(line.strip())

                        data2, data11, data13, data14 = self.analysis_line(line)

                        value1 = float(data11) + float(data13)
                        value2 = float(data14)
                        value3 = format(value1 / value2, '.2f')
                        eq_water.append(data2)
                        # eq_water.append(format(value1, '.2f'))
                        # eq_water.append(value3)
                        eq_water.append(data14)
                        eq_water.append(float(data14))
                    except Exception as e:
                        print(e)
                        eq_water = []

                if not line:
                    break
        return eq8, eq_ab9, eq_ab10, eq_ab11, eq_c9, eq_d9, eq_water

    @staticmethod
    def analysis_line(line):
        """
        用于解析除开110,111的其他case
        :param line:
        :return:
        """
        data = line.split()

        # 如果第5位 不是浮点数，长串     num
        try:
            flt = float(data[5])  # 是浮点数不会报错，执行try， 否则执行except
            return data[2], data[11], data[12], data[13]

        except ValueError as e:
            return data[2], data[12], data[13], data[14]

        # if data[-1] == '*':
        #     return data[2], data[-5], data[-3], data[-2]
        # else:
        #     return data[2], data[-4], data[-2], data[-1]

    @staticmethod
    def analysis_line2(line):
        """
        解析case110, case111
        :param line:
        :return:
        """
        data = line.split()
        # 如果第5位 不是浮点数，长串   num
        try:
            flt = float(data[5])    # 是浮点数不会报错，执行try， 否则执行except
            return data[2], data[10], data[11], data[12]

        except ValueError as e:
            return data[2], data[11], data[12], data[13]

        # 如果第5为是浮点数
        # if data[-1] == '*':
        #     return data[2], data[-4], data[-3], data[-2]
        # else:
        #     return data[2], data[-3], data[-2], data[-1]


class GetFreResult:
    def __init__(self, dir_path, fre_filename_list):
        self.dir_path = dir_path
        self.fre_filename_list = fre_filename_list
        # self.old_fre_path = fre_path

    def get_fre_files(self):

        # if os.path.exists(self.old_fre_path):
        #     name = os.path.basename(self.old_max_path)
        #     file_name = os.path.splitext(name)[0]
        #     eq8, eq_ab9, eq_ab10, eq_ab11, eq_c9, eq_d9, eq_water = self.deal_max_table(self.old_max_path, file_name)
        fre_data = {}
        if self.fre_filename_list:

            for m in self.fre_filename_list:
                start_index = 0
                end_index = 0

                fre_result_path = os.path.join(self.dir_path, m)
                name = os.path.basename(fre_result_path)
                file_name = os.path.splitext(name)[0]

                if os.path.exists(fre_result_path):
                    command_line = '\n'*2
                    try:
                        with open(fre_result_path, 'r', encoding='utf8') as f:
                            lines = f.readlines()
                    except UnicodeDecodeError:
                        with open(fre_result_path, 'r', encoding='gbk') as f:
                            lines = f.readlines()

                    for i, line in enumerate(lines):
                        if '*****原支吊架参数命令流****' in line:
                            print('是否进入这里')
                            start_index = i
                        if 'ENDP' in line:
                            end_index = i
                    # 判断下标

                    if start_index and end_index:
                        for line in lines[start_index: end_index]:
                            command_line += line + '\n'
                    fre_data[file_name] = command_line

        return fre_data











