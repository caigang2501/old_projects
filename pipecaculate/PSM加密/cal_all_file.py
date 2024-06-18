import os
from io import StringIO
import re

from PyQt5.QtWidgets import QMainWindow


class GenTmp(QMainWindow):
    def __init__(self, data_path, max_path, prr_path, ppo_path, prc_path):
        super().__init__()
        self.data_path = data_path
        self.list_equipment_nodes = []
        self.max_path = max_path
        self.prr_path = prr_path
        self.ppo_path = ppo_path
        self.prc_path = prc_path
        print(self.max_path)
        print(self.prr_path)
        print(self.ppo_path)
        print(self.prc_path)

    def gen_tmp(self):
        list_equipment_nodes = []
        name = os.path.basename(self.data_path)
        fre_name = os.path.splitext(name)[0]
        tmp_name = fre_name + '.tmp'
        tmp_path = os.path.join(os.path.dirname(self.data_path), tmp_name)
        output_data = open(tmp_path, 'w+')
        if self.data_path:
            self.deal_fre_table()
        if self.max_path:
            self.deal_max_table(output_data)

        if self.prr_path:
            self.deal_prr_table(output_data)

        if self.ppo_path:
            self.deal_appendix_1(output_data)

        if self.prc_path:
            self.deal_appendix_2(output_data)

        output_data.close()
        list_equipment_nodes.clear()
        return tmp_path

    def deal_fre_table(self):
        # m1 = re.search('RSTN', line, re.IGNORECASE)
        with open(self.data_path, 'r', errors='ignore') as f:

            while True:
                line = f.readline()
                if re.search('NOZZ', line, re.IGNORECASE):

                    temp = "ACTION OF PIPING ON RESTRAINT(S) AT POINT NO.  " + line.split()[1].split('=')[1].\
                        rjust(3, ' ')

                    self.list_equipment_nodes.append(temp)
                if not line:
                    break
            print(self.list_equipment_nodes)

    def deal_max_table(self, output_data):

        str_data = StringIO()
        is_write_info = False
        str1 = '****************************************************************************' + '\n'

        with open(self.max_path, 'r', errors='ignore') as f:

            while True:
                line = f.readline().strip('\n')
                # print(line)
                if "CALCULATION NUMBER" in line:
                    is_write_info = True
                    str_data.truncate(0)
                    str_data.seek(0)
                if is_write_info:
                    str_data.write(line+'\n')
                if "LOADING CASE NO. 108" in line:
                    output_data.write('\n')
                    output_data.write("@O级准则-方程8"+"\n")
                    for i in range(13):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())
                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO. 110" in line:
                    output_data.write('\n')
                    output_data.write("@AB级准则 方程10"+'\n')
                    str_data.truncate()

                    for i in range(15):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())

                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO. 111" in line:
                    output_data.write('\n')
                    output_data.write("@AB级准则 方程11"+'\n')

                    for i in range(13):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())

                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO.  209 " in line:
                    output_data.write('\n')
                    output_data.write("@单独由冲击（OBS）和摇摆作用下的管道最大应力比"+'\n')

                    for i in range(11):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())

                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO. 109" in line:
                    output_data.write('\n')
                    output_data.write("@单独由冲击（OBS）和摇摆作用下的管道最大应力比"+'\n')

                    for i in range(13):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())

                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    output_data.write('\n')
                    output_data.write("@AB级准则-方程9"+'\n')
                    # str_data.write('\n')
                    # str_data.write('\n')
                    # str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO.  709 " in line:
                    output_data.write('\n')
                    output_data.write("@单独由冲击（SSS）和摇摆作用下的管道最大应力比" + '\n')

                    for i in range(11):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())
                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)

                if "LOADING CASE NO. 140" in line:
                    output_data.write('\n')
                    output_data.write("@C级准则 方程9"+'\n')

                    for i in range(13):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())
                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO. 150" in line:
                    output_data.write('\n')
                    output_data.write("@D级准则 方程9"+'\n')

                    for i in range(13):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())

                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    output_data.write('\n')
                    output_data.write("@单独由冲击（SSS）和摇摆作用下的管道最大应力比"+'\n')
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if "LOADING CASE NO.  16" in line:
                    output_data.write('\n')
                    output_data.write("@水压试验"+'\n')

                    for i in range(11):
                        line = f.readline()
                        str_data.write(line)

                    line = f.readline()
                    str_data.write(line)

                    for i in range(9):
                        str_data.write(f.readline())
                    str_data.write('\n')
                    str_data.write('\n')
                    str_data.write(str1)
                    output_data.write(str_data.getvalue())
                    is_write_info = False

                if not line:
                    break

    def deal_prr_table(self, output_data):
        # 获取5.1节表格  共2个表格需要处理
        # 模型中节点	X	Y	Z
        # 数据来源：.prr文件

        str_data = StringIO()
        str_data1 = StringIO()
        str_data2 = StringIO()
        temp_data = StringIO()
        temp_data2 = StringIO()
        is_right = False
        first_1 = False
        first_2 = False
        first_11 = False
        first_22 = False
        j_30 = 0
        j_40 = 0
        str1 = '****************************************************************************' + '\n'
        with open(self.prr_path, 'r', errors='ignore') as f:
            print('prr')
            while True:
                line = f.readline()
                if "CALCULATION NUMBER" in line:
                    str_data.truncate(0)
                    str_data.seek(0)
                    str_data.write(line + '\n')
                    str_data.write(f.readline())
                    str_data.write(f.readline())

                if "LOADING CASE NO.   2" in line:
                    if not first_1:
                        first_1 = True
                        str_data1.write('\n')
                        str_data1.write("@OBS冲击摇摆计算得到的阀门最大加速度"+"\n")

                        str_data1.write(str_data.getvalue())
                        str_data.truncate(0)
                    temp_data.write(line)

                    for i in range(8):
                        line = f.readline()
                        if first_1:
                            temp_data.write(line)
                        if "GLOBAL BOUNDS" in line:
                            is_right = True

                    if not is_right:
                        temp_data.truncate(0)
                        temp_data.seek(0)
                        continue

                    if not first_11:
                        is_right = False
                        first_11 = True
                        str_data1.write(temp_data.getvalue())

                    temp_data.truncate(0)

                    while True:
                        line = f.readline()
                        if line[0] != ' ':
                            break

                        if "VALVE" in line:

                            str_data1.write(line)

                            j_30 += 1

                if "LOADING CASE NO.   9" in line:
                    if not first_2:
                        first_2 = True
                        str_data2.write('\n')
                        str_data2.write("@SSS冲击摇摆计算得到的阀门最大加速度"+"\n")
                        str_data2.write(str_data.getvalue())
                        str_data.truncate(0)

                    temp_data2.write(line)

                    for i in range(8):
                        line = f.readline()
                        if first_2:
                            temp_data2.write(line)
                        if "GLOBAL BOUNDS" in line:
                            is_right = True

                    if not is_right:
                        temp_data2.truncate(0)
                        temp_data2.seek(0)
                        continue

                    if not first_22:
                        first_22 = True
                        is_right = False
                        str_data2.write(temp_data2.getvalue())

                    # temp_data2.truncate(0)

                    while True:
                        line = f.readline()
                        if line[0] != ' ':
                            break

                        if "--VALVE--" in line:

                            str_data2.write(line)

                            j_40 += 1
                if not line:
                    break
        str_data1.write('\n')
        str_data1.write('\n')
        str_data1.write(str1)
        output_data.write(str_data1.getvalue())
        str_data2.write('\n')
        str_data2.write('\n')
        str_data2.write(str1)
        output_data.write(str_data2.getvalue())

    def deal_appendix_1(self, output_data):

        is_first = False  # 记录开始位置
        is_second = False  # 记录是否为需要的数据
        is_switch = False  # 是否是设备接管节点号
        str_data = StringIO()
        str_temp = ""
        index = 0

        with open(self.ppo_path, 'r', errors='ignore') as f:
            print('ppo')
            while True:
                line = f.readline()    # 读取行内容
                if line.startswith('='):
                    is_first = True
                    index = 0
                    is_second = False
                    str_data.truncate(0)
                    str_data.seek(0)
                    str_data.write(line)

                elif is_first:
                    if line.startswith('-'):
                        index += 1
                    str_data.write(line)
                    if "ACTION OF PIPING ON RESTRAINT(S) AT POINT NO.  " in line:
                        str_temp = line
                        is_second = True
                    if 2 == index and is_second:
                        is_first = False
                        for i in range(len(self.list_equipment_nodes)):
                            if self.list_equipment_nodes[i] in str_temp:
                                is_switch = True
                                # output_data.write("@设备接管+节点" + str_temp[47:51].strip())
                                # output_data.write(str_data.getvalue())
                                # str_data1.write(str_data.getvalue())
                                break
                        if not is_switch:
                            output_data.write("@支撑+节点" + str_temp[47: 51].strip()+'\n')
                            output_data.write(str_data.getvalue())

                    is_switch = False
                if not line:
                    break
        is_switch = False
        is_first = False
        is_second = False
        str_data3 = StringIO()
        str_temp1 = ''

        with open(self.ppo_path, 'r') as f:
            while True:
                line = f.readline().strip('\n')
                if line.startswith("="):
                    is_first = True
                    index = 0
                    is_second = False
                    str_data3.truncate(0)
                    str_data3.seek(0)
                    str_data3.write(line+'\n')
                elif is_first:
                    if line.startswith('-'):
                        index += 1
                    str_data3.write(line + '\n')
                    if "ACTION OF PIPING ON RESTRAINT(S) AT POINT NO.  " in line:
                        str_temp1 = line
                        is_second = True
                    if 2 == index and is_second:
                        is_first = False
                        for i in range(len(self.list_equipment_nodes)):
                            if self.list_equipment_nodes[i] in str_temp1:
                                is_switch = True
                                output_data.write("@设备接管+节点" + str_temp1[47:51].strip() + '\n')
                                output_data.write(str_data3.getvalue())
                                str_data3.truncate(0)
                                str_data3.seek(0)
                                break

                if not line:
                    break

    def deal_appendix_2(self, output_data):

        index = 0
        num = 0
        is_first = False  # 记录开始位置
        is_second = False  # 记录是否为需要的数据
        is_third = False  # 是否是设备接管节点号
        is_many_data = False
        str_data = StringIO()
        str_data1 = StringIO()

        with open(self.prc_path, 'r', errors='ignore') as f:
            print('prr')
            while True:
                line = f.readline()
                if "CALCULATION NUMBER" in line:  # 寻找标志数据
                    is_first = True
                    index = 0
                    str_data.truncate(0)
                    str_data.seek(0)

                    if not is_many_data:
                        str_data.write(line)
                elif is_first:
                    if not line.startswith(' '):
                        index += 1
                    if "LOADING CASE NO. 150" in line:
                        is_second = True
                    if "GLOBAL ---DISPLACEMENTS (MM)---    --ROTATIONS (RAD*1000)--       ------ACCEL (G-S)------" in line:
                        is_third = True
                    if 1 == index & is_second & is_third:
                        is_first = False
                        is_second = False
                        is_third = False
                        is_many_data = True
                        num = 0
                        str_data1.write(str_data.getvalue())
                    if is_many_data:
                        num += 1
                        if num > 11:
                            str_data.write(line)
                    else:
                        str_data.write(line)
                if not line:
                    break
        output_data.write("@位移输出" + '\n')
        if str_data1:
            output_data.write(str_data1.getvalue())

        else:
            output_data.write("empty")
