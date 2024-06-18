from copy import copy
from pprint import pprint


class GenRefLines:
    def __init__(self):
        pass

    def get_new_lines(self, kinds, new_nodes, k_name, old_line, lv):
        """
        :param kinds:
        :param new_nodes:
        :param k_name: 'RSTN',
        :return:
        """
        self.lv = lv

        all_lines = []
        for i in kinds:
            for item in new_nodes:
                new_lines1 = '*********原支吊架参数命令流*************' + '\n'
                new_lines1 += old_line
                new_lines = '\n' + '*********优化后支吊架参数命令流**********' + '\n'
                new_lines1 += new_lines

                for k, v in item.items():
                    h = i.copy()
                    h['PT'] = v
                    new_node_line = self.update_new_line(h, k_name)
                    new_lines1 += new_node_line
                all_lines.append(new_lines1)
        return all_lines

    def get_new_lines_more(self, all_lines, kinds, new_nodes, k_name, lv):
        """

        :param kinds:
        :param new_nodes:
        :param k_name: 'RSTN',
        :return:
        """

        # print('=================================================================')
        # pprint(kinds)
        # pprint(new_nodes)
        # print('===================================================================')
        self.lv = lv
        for i in kinds:
            for item in new_nodes:

                new_lines = ''

                h = i.copy()
                h['PT'] = item
                new_node_line = self.update_new_line(h, k_name)
                new_lines += new_node_line
                pprint(new_lines)
                all_lines[item].append(new_lines)
        pprint(all_lines)
        return all_lines

    def update_new_line(self, new_d, k_name):
        """
        用于生成支吊架命令行
        :param new_d: 已经形成的数据字典
        :param k_name: 支吊架类型
        :return: 已经生成的命令行
        """

        if 'DX' in new_d.keys() and 'DY' in new_d.keys() and new_d['DX'] == '1' and new_d['DY'] == '1' \
                and 'DZ' in new_d.keys() and new_d['DZ'] == '0':
            two_line = self.make_two_line(new_d, k_name, 'DX', 'DY')
            node_line = two_line

        elif 'DX' in new_d.keys() and 'DZ' in new_d.keys() and new_d['DX'] == '1' and new_d['DZ'] == '1' \
                and 'DY' in new_d.keys() and new_d['DY'] == '0':
            two_line = self.make_two_line(new_d, k_name, 'DX', 'DZ')
            node_line = two_line
        elif 'DY' in new_d.keys() and 'DZ' in new_d.keys() and new_d['DY'] == '1' and new_d['DZ'] == '1' \
                and 'DX' in new_d.keys() and new_d['DX'] == '0':
            two_line = self.make_two_line(new_d, k_name, 'DY', 'DZ')
            node_line = two_line
        elif 'DX' in new_d.keys() and 'DZ' in new_d.keys() and 'DY' in new_d.keys() and new_d['DX'] == '1' \
                and new_d['DY'] == '1' and new_d['DZ'] == '1':
            three_line = self.make_three_line(new_d, k_name)
            node_line = three_line
        elif 'DX' in new_d.keys() and 'DY' in new_d.keys() and new_d['DX'] == '1' and new_d['DY'] == '1' \
                and 'DZ' not in new_d.keys():
            two_line = self.make_two_line(new_d, k_name, 'DX', 'DY')
            node_line = two_line

        elif 'DX' in new_d.keys() and 'DZ' in new_d.keys() and new_d['DX'] == '1' and new_d['DZ'] == '1' \
                and 'DY' not in new_d.keys():
            two_line = self.make_two_line(new_d, k_name, 'DX', 'DZ')
            node_line = two_line

        elif 'DY' in new_d.keys() and 'DZ' in new_d.keys() and new_d['DY'] == '1' and new_d['DZ'] == '1' \
                and 'DX' not in new_d.keys():
            two_line = self.make_two_line(new_d, k_name, 'DY', 'DZ')
            node_line = two_line

        else:
            one_line = self.make_node_line(new_d, k_name)
            node_line = one_line
        return node_line

    def make_three_line(self, hanger_input, k_name):
        # three_line = ''

        hanger_input['DX'] = '0'
        hanger_input['DY'] = '1'
        hanger_input['DZ'] = '0'

        line1 = self.make_node_line(hanger_input, k_name)
        hanger_input['DX'] = '1'
        hanger_input['DY'] = '0'
        hanger_input['DZ'] = '0'
        line2 = self.make_node_line(hanger_input, k_name)

        hanger_input['DX'] = '0'
        hanger_input['DY'] = '0'
        hanger_input['DZ'] = '1'

        line3 = self.make_node_line(hanger_input, k_name)
        three_line = line1 + line2 + line3

        return three_line

    def make_two_line(self, hanger_input, k_name, k1, k2):
        two_line = ''
        if k1 == 'DX' and k2 == 'DY':
            hanger_input['DX'] = '0'
            line1 = self.make_node_line(hanger_input, k_name)
            hanger_input['DX'] = '1'
            hanger_input['DY'] = '0'
            line2 = self.make_node_line(hanger_input, k_name)
            two_line = line1 + line2
        if k1 == 'DX' and k2 == 'DZ':
            hanger_input['DX'] = '0'
            line1 = self.make_node_line(hanger_input, k_name)
            hanger_input['DX'] = '1'
            hanger_input['DZ'] = '0'
            line2 = self.make_node_line(hanger_input, k_name)
            two_line = line1 + line2

        if k1 == 'DY' and k2 == 'DZ':
            hanger_input['DY'] = '0'
            line1 = self.make_node_line(hanger_input, k_name)
            hanger_input['DY'] = '1'
            hanger_input['DZ'] = '0'
            line2 = self.make_node_line(hanger_input, k_name)
            two_line = line1 + line2
        return two_line

    def make_node_line(self, hanger_input, k_name):
        if self.lv:
            lv_line = 'LV='+self.lv
            write_case = k_name + ' '
            pt_str = 'PT=' + str(hanger_input['PT']) + ' '
            write_case = write_case + pt_str
            new_dict = copy(hanger_input)
            del new_dict['PT']
            for k, v in new_dict.items():
                if hanger_input[k]:
                    parm = str(k) + '=' + str(v) + ' '
                    write_case += parm

            end_case = write_case + lv_line + '\n'
            return end_case
        else:
            write_case = k_name + ' '
            pt_str = 'PT=' + str(hanger_input['PT']) + ' '
            write_case = write_case + pt_str
            new_dict = copy(hanger_input)
            del new_dict['PT']
            for k, v in new_dict.items():
                if hanger_input[k]:
                    parm = str(k) + '=' + str(v) + ' '
                    write_case += parm

            end_case = write_case + '\n'
            return end_case





