#pyinstaller -w PSM.py --hidden-import lxml._elementpath


import re
import sys
import os
import json
import shutil
import datetime
import itertools
from io import StringIO
from PyQt5 import QtGui, QtCore
from parse_xml import *
from cal_all_file import GenTmp
from show_fre_result import GetMaxResult, GetFreResult
from gen_ref_lines import GenRefLines
from export_report_new import ExportReport
from report3 import Ui_MainWindow
from shock_spectrum import ShockSpectrum
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtCore import Qt, QFileInfo, QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem, \
    QFileIconProvider, QMenu, QHeaderView, QTableWidgetItem, QInputDialog, QListWidgetItem,QWidget,\
    QVBoxLayout,QGroupBox,QLineEdit,QGridLayout,QLabel,QPushButton,QTextBrowser


class ActivationWidget(QMainWindow):
    def __init__(self, parent=None):
        super(ActivationWidget, self).__init__(parent)

        self.maptable = [['x','m','Q','a','g','E','u','O',9,'t'],
            [8,1,'F','P','b','s','v','W','k',5],
            [6,'G','P','w','Y','E',0,9,'r','c'],
            [3,'H',0,'x','O','d','R','z','q',9],
            ['Q','V','c','p','X','y','I',4,'e',2],
            [7,4,'R',2,'o','J','z','U','f',1],
            ['S','A','v','Z',6,'n','K','g','L','h'],
            [5,'l','m','h','B','T','j','S','A','W'],
            ['k','b','I','M','D',1,'Y','l','C','n'],
            ['i',8,'N','U','F',3,7,'D','j','T']]

        self.MACADDRESS = self.get_macaddress()
        self.DATETIME = str(datetime.datetime.now())[:10]

        self.setWindowTitle("许可文件验证")
        self.resize(600, 400)
        self.setCentralWidget(QWidget())
        self.main_layout = QVBoxLayout(self.centralWidget())
        
        self.holder = QGroupBox()
        vbox = QGridLayout()

        self.macadressline = QTextBrowser()
        self.macadressline.setText(self.MACADDRESS)
        self.macadressline.setFixedHeight(25)
        lb1 = QLabel('你的物理地址是:')
        vbox.addWidget(lb1,0,3,1,1)
        vbox.addWidget(self.macadressline,0,5,1,1)


        self.activationpath = QLineEdit()
        self.activationpath.setObjectName('activationpath')
        lb2 = QLabel('许可文件路径:')
        vbox.addWidget(lb2,1,3,1,1)
        vbox.addWidget(self.activationpath,1,5,1,1)
        self.savepathbutton = QPushButton()
        self.savepathbutton.setText("选择路径")
        vbox.addWidget(self.savepathbutton,1,10,1,3)
        self.savepathbutton.clicked.connect(self.choosepath)

        self.holder.setLayout(vbox)
        self.main_layout.addWidget(self.holder)
        #self.savepathbutton.clicked.connect(self.choosepath)
        # self.holder.hide()

        self.loginbutton = QPushButton()
        self.loginbutton.setText("验证")
        self.main_layout.addWidget(self.loginbutton)
        self.loginbutton.clicked.connect(self.bind)

        # with open('licence.txt', "r",encoding='UTF-8') as file:
        #     text = file.read()
        # licence = self.get_verify_code()
        # if text == licence:
        #     demo.show()
        # else:
        #     bindwidget.show()
    
    
    def choosepath(self):
        savepath = QFileDialog.getOpenFileName(self, "选择路径")
        self.activationpath.setText(savepath[0])

    def get_verify_code(self,cutofftime):
        Etherstr = ''
        etable = {'A':'10','B':'11','C':'12','D':'13','E':'14','F':'15'}
        for c in self.MACADDRESS+cutofftime:
            if c.isalpha() or c.isdigit(): 
                if c.isalpha():
                    Etherstr += str(int(etable[c.upper()])%10)          
                else:
                    Etherstr += c  

        # 扩展至20位
        # i = 0
        # Etherstr1 = ""
        # for x in Etherstr:
        #     Etherstr1 += str((int(x)+int(Etherstr[i+2]))%10)
        # Etherstr = (Etherstr+Etherstr1)[0:20]

        sum = 0
        for x in Etherstr:
            sum += int(x)
        sum = sum%10

        licence = ''
        i = 0
        for x in Etherstr:
            licence += str(self.maptable[((sum+i+int(x))%10)][int(x)])
            i += 1       
        return licence
    
    def verify(self,lscpath):
        text = ""
        try:
            with open(lscpath, "r",encoding='UTF-8') as file:
                text = file.read()
        except FileNotFoundError:
            pass
        
        timeout = self.datefoemate(str(datetime.datetime.now())[:10])>self.datefoemate(text[20:])
        if text[0:20] == self.get_verify_code(text[20:]) and not timeout:
            return True

        return False

    def bind(self):
        if self.verify(self.get_value('activationpath')):
            with open(self.get_value('activationpath'), "r",encoding='UTF-8') as file:
                text = file.read()
            with open('licence.txt', "w",encoding='UTF-8') as file:
                file.write(text)
            bindwidget.hide()
            demo.show()
        else:
            QMessageBox.critical(
                None,
                '错误',
                '许可文件未通过验证，请选择正确的许可文件')  

    def get_macaddress(self):
        mac = None
        if sys.platform == "win32":
            isEther = False
            for line in os.popen("ipconfig /all"):
                # if line.lstrip().startswith("物理地址"):
                if '以太网' in line:
                    isEther = True
                if isEther and '物理地址' in line:
                    # mac = line.split(":")[1].strip().replace("-", ":")
                    mac = line.split(":")[1].strip()
                    break
        else:
            isEther = False
            for line in os.popen("/sbin/ipconfig"):
                if '以太网' in line:
                    isEther = True
                if isEther and '物理地址' in line:
                    mac = line.split(":")[1].strip()
                    break
        return mac

    def datefoemate(self,date):
        newdate = ""
        for c in date:
            if c.isdigit():
                newdate += c

        return newdate

    def get_value(self, object_name):
        try:
            return self.findChild(QLineEdit, object_name).text()
        except Exception as e:
            print(object_name)


def get_default_path(key):
    """获取用户操作某个文件时，上一次读取文件的路劲吧
    :param key : 文件的key
    """

    # 第一次不存在改记录文件
    try:

        if not os.path.exists("./default_path.json"):
            default_path = {
                "fre_dir": "./",
                "materials_dir": "./"
            }
            with open("./default_path.json", "w") as f:
                json.dump(default_path, f)
        else:
            with open("./default_path.json", "r") as f:
                default_path = json.load(f)

        alt = default_path[key]
        return alt
    except Exception as e:
        return r"./"  # 获取失败返回当前目录


def set_default_path(key, path):
    """设置某个文件的默认查找路径
    key：文件类型
    path ：目录路径
    """

    with open("./default_path.json", "r+") as f:
        default_path = json.load(f)

        default_path[key] = path

        # 清空读取原来的 json 内容，写入新的内容
        f.seek(0)
        f.truncate()
        json.dump(default_path, f)


class DemoMain(QMainWindow, Ui_MainWindow):
    # 此类用于链接界面控件和后台函数

    dom = ''  # 文档对象
    tmp_path = ''  # 计算结果路径
    library_path = ''  # 材料库路径
    first_init_math = False
    first_init_matd = False
    reg0 = QRegExp('[A-Z0-9,，-]+$')
    va1 = QRegExpValidator()
    va1.setRegExp(reg0)
    reg1 = QRegExp('[0-9A-Z]+$')
    va2 = QRegExpValidator()
    va2.setRegExp(reg1)
    reg2 = QRegExp('[0-9,.，]+$')
    va3 = QRegExpValidator()
    va3.setRegExp(reg2)
    reg3 = QRegExp('[0-1,，]+')
    va4 = QRegExpValidator()
    va4.setRegExp(reg3)

    reg4 = QRegExp('^(0|[1-9][0-9]*)$')
    va5 = QRegExpValidator()
    va5.setRegExp(reg4)

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 调用Ui_Mainwindow中的函数setupUi实现显示界面

        # 绑定信号和槽函数部分
        self.max_path = ''
        self.data_path = ''
        self.prd_path = ''

        self.action_config.triggered.connect(self.page_show)
        self.actionReport_2.triggered.connect(self.page3_show)
        self.action_view.triggered.connect(self.page1_show)
        self.actionExit_2.triggered.connect(self.page1_show)
        self.actionHanger.triggered.connect(self.page4_show)
        self.actionMaterials.triggered.connect(self.page2_show)
        self.actionExit_2.triggered.connect(self.closeEvent)
        self.actionShock_Spectrum.triggered.connect(self.page5_show)
        self.conf_data.clicked.connect(self.button_data_click)
        self.save_conf.clicked.connect(self.button_save_conf)

        self.button_ouput.clicked.connect(self.button_output_click)
        self.button_modul.clicked.connect(self.button_modul_click)
        self.button_run.clicked.connect(self.button_run_click)

        # 冲击谱一栏
        self.pushButton_2.clicked.connect(self.button_get_shock)
        self.pushButton_3.clicked.connect(self.button_get_shock2)
        self.pushButton_4.clicked.connect(self.button_gen_ref)
        self.pushButton_5.clicked.connect(self.button_gen_ref2)
        self.listWidget_7.itemClicked.connect(self.shock_item_click)
        # 设置文件属性展示框不能被编辑

        self.lineEdit1.setFocusPolicy(Qt.NoFocus)
        self.lineEdit2.setFocusPolicy(Qt.NoFocus)
        self.lineEdit3.setFocusPolicy(Qt.NoFocus)
        self.lineEdit4.setFocusPolicy(Qt.NoFocus)
        self.lineEdit5.setFocusPolicy(Qt.NoFocus)
        self.lineEdit6.setFocusPolicy(Qt.NoFocus)
        self.lineEdit7.setFocusPolicy(Qt.NoFocus)
        self.lineEdit8.setFocusPolicy(Qt.NoFocus)
        self.lineEdit9.setFocusPolicy(Qt.NoFocus)
        self.lineEdit10.setFocusPolicy(Qt.NoFocus)
        self.lineEdit11.setFocusPolicy(Qt.NoFocus)
        self.lineEdit12.setFocusPolicy(Qt.NoFocus)

        self.treeWidget_2.itemClicked.connect(self.deal_file)  # 文件单击显示属性
        self.treeWidget_2.itemDoubleClicked.connect(self.skim_file)  # 双击展示文件内容

        # 点击结果浏览界面函数绑定
        self.listWidget.itemClicked.connect(self.list_item_index_changed)
        self.listWidget_2.itemClicked.connect(self.list_item_index_changed)
        self.listWidget_3.itemClicked.connect(self.list_item_index_changed)
        self.listWidget_4.itemClicked.connect(self.list_item_index_changed)
        self.listWidget_5.itemClicked.connect(self.list_item_index_changed)

        # 单支吊架优化
        self.gen_fre_ref.clicked.connect(self.replace_spec)
        # 多支吊架优化
        self.gen_fre_ref_2.clicked.connect(self.replace_spec)

        # 配置支吊架结果文件夹
        self.pushButton.clicked.connect(self.button_get_result)
        self.lineEdit_3.setValidator(self.va1)
        self.lineEdit_4.setValidator(self.va2)
        self.lineEdit_4.editingFinished.connect(self.show_node)  # 待优化的支吊架节点
        self.lineEdit_3.editingFinished.connect(self.show_node2)  # 拟优化位置节点号

        lineedits1 = [self.RSTN_DX, self.RSTN_DY, self.RSTN_DZ,
                      self.RSUP_DX, self.RSUP_DY, self.RSUP_DZ,
                      self.HANG_DX, self.HANG_DY, self.HANG_DZ,
                      self.SNUB_DX, self.SNUB_DY, self.SNUB_DZ]
        lineedits2 = [self.RSTN_SP, self.RSUP_SP, self.HANG_SP, self.SNUB_SP]

        for line_e in lineedits1:
            line_e.setValidator(self.va4)

        for line_e2 in lineedits2:
            line_e2.setValidator(self.va3)

        # 支吊架结果浏览模块

        # 点击应力比小于1
        self.listWidget_6.itemClicked.connect(self.get_hanger_data6)
        # 支吊架优化后计算结果浏览
        self.listWidget_8.itemClicked.connect(self.get_hanger_data)
        # 点击支吊架优化命令
        self.listWidget_9.itemClicked.connect(self.get_hanger_data3)

        # 多支吊架模块
        self.lineEdit_5.setValidator(self.va2)
        self.lineEdit_10.setValidator(self.va2)
        self.lineEdit_12.setValidator(self.va2)

        self.lineEdit_9.setValidator(self.va1)
        self.lineEdit_11.setValidator(self.va1)
        self.lineEdit_13.setValidator(self.va1)

        self.lineEdit_5.editingFinished.connect(self.show_node3)
        self.lineEdit_10.editingFinished.connect(self.show_node4)
        self.lineEdit_12.editingFinished.connect(self.show_node5)

        self.lineEdit_9.editingFinished.connect(self.show_node9)
        self.lineEdit_11.editingFinished.connect(self.show_node11)
        self.lineEdit_13.editingFinished.connect(self.show_node13)

        lvs = [self.RSTN_LV, self.SNUB_LV, self.RSUP_LV, self.HANG_LV,
               self.RSTN_LV_2, self.SNUB_LV_2, self.RSUP_LV_2, self.HANG_LV_2,
               self.RSTN_LV_3, self.SNUB_LV_3, self.RSUP_LV_3, self.HANG_LV_3,
               self.RSTN_LV_4, self.SNUB_LV_4, self.RSUP_LV_4, self.HANG_LV_4
               ]
        for lv in lvs:
            lv.setValidator(self.va5)

        lineedits3 = [self.RSTN_DX_2, self.RSTN_DY_2, self.RSTN_DZ_2,
                      self.RSUP_DX_2, self.RSUP_DY_2, self.RSUP_DZ_2,
                      self.HANG_DX_2, self.HANG_DY_2, self.HANG_DZ_2,
                      self.SNUB_DX_2, self.SNUB_DY_2, self.SNUB_DZ_2]
        lineedits4 = [self.RSTN_SP_2, self.RSUP_SP_2, self.HANG_SP_2, self.SNUB_SP_2]

        for line_e in lineedits3:
            line_e.setValidator(self.va4)

        for line_e2 in lineedits4:
            line_e2.setValidator(self.va3)

        lineedits5 = [self.RSTN_DX_3, self.RSTN_DY_3, self.RSTN_DZ_3,
                      self.RSUP_DX_3, self.RSUP_DY_3, self.RSUP_DZ_3,
                      self.HANG_DX_3, self.HANG_DY_3, self.HANG_DZ_3,
                      self.SNUB_DX_3, self.SNUB_DY_3, self.SNUB_DZ_3]
        lineedits6 = [self.RSTN_SP_3, self.RSUP_SP_3, self.HANG_SP_3, self.SNUB_SP_3]

        for line_e in lineedits5:
            line_e.setValidator(self.va4)

        for line_e2 in lineedits6:
            line_e2.setValidator(self.va3)

        lineedits7 = [self.RSTN_DX_4, self.RSTN_DY_4, self.RSTN_DZ_4,
                      self.RSUP_DX_4, self.RSUP_DY_4, self.RSUP_DZ_4,
                      self.HANG_DX_4, self.HANG_DY_4, self.HANG_DZ_4,
                      self.SNUB_DX_4, self.SNUB_DY_4, self.SNUB_DZ_4]
        lineedits8 = [self.RSTN_SP_4, self.RSUP_SP_4, self.HANG_SP_4, self.SNUB_SP_4]

        for line_e in lineedits7:
            line_e.setValidator(self.va4)

        for line_e2 in lineedits8:
            line_e2.setValidator(self.va3)

        try:
            self.open_materials.clicked.connect(self.button_material_click)  # 打开材料库
            self.save_materials.clicked.connect(self.button_save_click)  # 存储材料库

            self.button_add.clicked.connect(self.add_row)  # 增加一行
            self.button_delete.clicked.connect(self.del_row)  # 删除一行
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.tableWidget.horizontalHeader().setStyleSheet('QHeaderView::section{background:SkyBlue}')
            self.tableWidget.verticalHeader().setStyleSheet('QHeaderView::section{background:SkyBlue}')

            self.treeWidget.itemClicked.connect(self.item_click)
            self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
            self.treeWidget.customContextMenuRequested.connect(self.right_click_menu)

        except Exception as e:
            pass

        self.RSTN.stateChanged.connect(self.choose)
        self.SNUB.stateChanged.connect(self.choose)
        self.RSUP.stateChanged.connect(self.choose)
        self.HANG.stateChanged.connect(self.choose)

        self.RSTN_2.stateChanged.connect(self.choose)
        self.SNUB_2.stateChanged.connect(self.choose)
        self.RSUP_2.stateChanged.connect(self.choose)
        self.HANG_2.stateChanged.connect(self.choose)

        self.RSTN_3.stateChanged.connect(self.choose)
        self.SNUB_3.stateChanged.connect(self.choose)
        self.RSUP_3.stateChanged.connect(self.choose)
        self.HANG_3.stateChanged.connect(self.choose)

        self.RSTN_4.stateChanged.connect(self.choose)
        self.SNUB_4.stateChanged.connect(self.choose)
        self.RSUP_4.stateChanged.connect(self.choose)
        self.HANG_4.stateChanged.connect(self.choose)

    def shock_item_click(self, item):
        """
        点击冲击谱分类，获得冲击谱
        :param item: 水面船体、水面甲板、潜艇船体、潜艇甲板
        :return:
        """
        chose_item = item.text()
        self.textBrowser_3.clear()
        try:
            if self.m_f_lines:
                show_content = self.m_f_lines[chose_item]
                # self.textBrowser_3.setText(show_content)
                if chose_item == '水面船体':
                    self.textBrowser_3.setText(show_content)
                if chose_item == '水面甲板':
                    self.textBrowser_3.setText(show_content)
                if chose_item == '潜艇船体':
                    self.textBrowser_3.setText(show_content)
                if chose_item == '潜艇甲板':
                    self.textBrowser_3.setText(show_content)
        except AttributeError as e:
            QMessageBox.information(self, '提示', '请先点击生成冲击谱计算！')

    def replace_spec(self):
        """
        批量替换fre文件中lv=1的水面船体、水面甲板、潜艇船体、潜艇甲板
        :return:
        """
        if self.data_path:

            try:
                # self.dir_num1 = 1
                # self.dir_num2 = 1

                if self.data_path:
                    fre_dir = os.path.dirname(self.data_path)
                    directory = QFileDialog.getExistingDirectory(None, "选取文件夹", fre_dir)  # 起始路径
                else:
                    directory = QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
                if directory:
                    prd_file_list = []
                    fre_file_list = []
                    p0 = []
                    f0 = []
                    # 遍历文件夹，查看对应的prd和fre文件
                    root, dirs, files = list(os.walk(directory))[0]
                    for file in files:
                        if os.path.splitext(file)[1] == '.prd':
                            p = os.path.splitext(file)[0]
                            p0.append(p)
                            data_max = os.path.join(directory, file)

                            prd_file_list.append(data_max)
                        if os.path.splitext(file)[1] == '.fre':
                            f = os.path.splitext(file)[0]
                            f0.append(f)
                            data_fre = os.path.join(directory, file)
                            fre_file_list.append(data_fre)

                    file_dict = {os.path.join(directory, i + '.prd'): os.path.join(directory, j + '.fre') for i in p0
                                 for j in f0 if i == j}
                    if file_dict:
                        new_fre1_dir = os.path.join(directory, 'optimization')
                        new_shock_dir = os.path.join(directory, 'spec_result')
                        spec_solver = os.path.join(directory, 'spec_solver')

                        if os.path.exists(spec_solver):
                            shutil.rmtree(spec_solver)
                            os.makedirs(spec_solver)
                        else:
                            os.makedirs(spec_solver)

                        if os.path.exists(new_fre1_dir):
                            shutil.rmtree(new_fre1_dir)
                            os.makedirs(new_fre1_dir)

                        else:
                            os.makedirs(new_fre1_dir)

                        if os.path.exists(new_shock_dir):
                            shutil.rmtree(new_shock_dir)
                            os.makedirs(new_shock_dir)
                        else:
                            os.makedirs(new_shock_dir)

                        for prd_path, fre_path in file_dict.items():

                            # 打开prd文件，生成对应的冲击谱，生成四个部分，根据用户选择，提取对应的结果
                            # 打开fre文件，写入对应的替换行，保存成新的文件
                            # self.textBrowser_3.clear()

                            total_mass, frequency = ShockSpectrum().cal_shock(prd_path)

                            if len(total_mass.keys()) == len(frequency.keys()):
                                # 冲击谱路径，以及各项内容

                                filepath, tmpfilename = os.path.split(prd_path)
                                shotname, extension = os.path.splitext(tmpfilename)
                                new_fre = os.path.join(new_fre1_dir, 'shock_%s.fre' % shotname)
                                shock_path, shock_lines = ShockSpectrum().cal_a_v(total_mass, frequency, new_shock_dir,
                                                                                  shotname)

                                replace_line = shock_lines[self.chose_radio]
                                self.replace_fre(fre_path, new_fre, replace_line)

                            else:
                                QMessageBox.information(self, '提示', '1个prd数据读取不匹配！请检查下源文件')
                        show_path1 = new_fre1_dir.replace('\\', '/')
                        QMessageBox.information(self, '提示', '完成！保存在:\n%s' % show_path1)

                        # 移动文件
                        root, dirs, files = list(os.walk(directory))[0]
                        for file in files:
                            old_file_path = os.path.join(directory, file)
                            new_file_path = os.path.join(spec_solver, file)
                            try:
                                shutil.move(old_file_path, new_file_path)
                            except OSError:
                                pass
                    else:
                        QMessageBox.information(self, '提示', '缺少fre或prd文件！')
            except Exception as e:
                print(e, '异常提示')
        else:
            QMessageBox.information(self, '提示', '请先配置文件！')

    @staticmethod
    def replace_fre(fre_path, new_fre, replace_line):
        """
        替换fre文件
        :param fre_path: 原来的fre文件
        :param new_fre: 新的fre文件
        :param replace_line: 替换的行
        :return:
        """
        flag = False
        a = ''
        b = ''
        with open(fre_path, 'r', encoding='utf8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if 'LV=1' in line:
                    print(line)
                    a = i + 1
                    flag = True
                elif line.strip().startswith("LV=2") and flag:
                    print(lines[i])
                    print(1)
                    b = i - 1
                    break
                elif line.startswith('*') and flag:
                    print(lines[i])
                    print(2)
                    b = i - 1
                    break
                elif line.startswith('=') and flag:
                    print(lines[i])
                    print(3)
                    b = i - 1
                    break
        with open(new_fre, 'a') as f:
            f.writelines(lines[:a])
            f.write(replace_line)
            f.writelines(lines[b:])

    def choose(self):
        """
        选择支吊架类型触发的事件
        :return:
        """
        if self.RSTN.isChecked():
            self.RSTN_DX.setDisabled(False)
            self.RSTN_DY.setDisabled(False)
            self.RSTN_DZ.setDisabled(False)
            self.RSTN_SP.setDisabled(False)
            self.RSTN_LV.setDisabled(False)
            self.RSTN_DX.setStyleSheet('background-color: white;')
            self.RSTN_DY.setStyleSheet('background-color: white;')
            self.RSTN_DZ.setStyleSheet('background-color: white;')
            self.RSTN_SP.setStyleSheet('background-color: white;')
            self.RSTN_LV.setStyleSheet('background-color: white;')

        else:
            self.RSTN_DX.setDisabled(True)
            self.RSTN_DY.setDisabled(True)
            self.RSTN_DZ.setDisabled(True)
            self.RSTN_SP.setDisabled(True)
            self.RSTN_LV.setDisabled(True)
            self.RSTN_DX.setStyleSheet('background-color: LightGray;')
            self.RSTN_DY.setStyleSheet('background-color: LightGray;')
            self.RSTN_DZ.setStyleSheet('background-color: LightGray;')
            self.RSTN_SP.setStyleSheet('background-color: LightGray;')
            self.RSTN_LV.setStyleSheet('background-color: LightGray;')
            self.RSTN_DX.clear()
            self.RSTN_DY.clear()
            self.RSTN_DX.clear()
            self.RSTN_SP.clear()
            self.RSTN_LV.clear()
        if self.SNUB.isChecked():
            self.SNUB_DX.setDisabled(False)
            self.SNUB_DY.setDisabled(False)
            self.SNUB_DZ.setDisabled(False)
            self.SNUB_SP.setDisabled(False)
            self.SNUB_LV.setDisabled(False)
            self.SNUB_DX.setStyleSheet('background-color: white;')
            self.SNUB_DY.setStyleSheet('background-color: white;')
            self.SNUB_DZ.setStyleSheet('background-color: white;')
            self.SNUB_SP.setStyleSheet('background-color: white;')
            self.SNUB_LV.setStyleSheet('background-color: white;')

        else:
            self.SNUB_DX.setDisabled(True)
            self.SNUB_DY.setDisabled(True)
            self.SNUB_DZ.setDisabled(True)
            self.SNUB_SP.setDisabled(True)
            self.SNUB_LV.setDisabled(True)
            self.SNUB_DX.setStyleSheet('background-color: LightGray;')
            self.SNUB_DY.setStyleSheet('background-color: LightGray;')
            self.SNUB_DZ.setStyleSheet('background-color: LightGray;')
            self.SNUB_SP.setStyleSheet('background-color: LightGray;')
            self.SNUB_LV.setStyleSheet('background-color: LightGray;')
            self.SNUB_DX.clear()
            self.SNUB_DY.clear()
            self.SNUB_DX.clear()
            self.SNUB_SP.clear()
            self.SNUB_LV.clear()

        if self.RSUP.isChecked():
            self.RSUP_DX.setDisabled(False)
            self.RSUP_DY.setDisabled(False)
            self.RSUP_DZ.setDisabled(False)
            self.RSUP_SP.setDisabled(False)
            self.RSUP_LV.setDisabled(False)
            self.RSUP_DX.setStyleSheet('background-color: white;')
            self.RSUP_DY.setStyleSheet('background-color: white;')
            self.RSUP_DZ.setStyleSheet('background-color: white;')
            self.RSUP_SP.setStyleSheet('background-color: white;')
            self.RSUP_LV.setStyleSheet('background-color: white;')

        else:
            self.RSUP_DX.setDisabled(True)
            self.RSUP_DY.setDisabled(True)
            self.RSUP_DZ.setDisabled(True)
            self.RSUP_SP.setDisabled(True)
            self.RSUP_LV.setDisabled(True)
            self.RSUP_DX.setStyleSheet('background-color: LightGray;')
            self.RSUP_DY.setStyleSheet('background-color: LightGray;')
            self.RSUP_DZ.setStyleSheet('background-color: LightGray;')
            self.RSUP_SP.setStyleSheet('background-color: LightGray;')
            self.RSUP_LV.setStyleSheet('background-color: LightGray;')
            self.RSUP_DX.clear()
            self.RSUP_DY.clear()
            self.RSUP_DX.clear()
            self.RSUP_SP.clear()
            self.RSUP_LV.clear()

        if self.HANG.isChecked():
            self.HANG_DX.setDisabled(False)
            self.HANG_DY.setDisabled(False)
            self.HANG_DZ.setDisabled(False)
            self.HANG_SP.setDisabled(False)
            self.HANG_LV.setDisabled(False)
            self.HANG_DX.setStyleSheet('background-color: white;')
            self.HANG_DY.setStyleSheet('background-color: white;')
            self.HANG_DZ.setStyleSheet('background-color: white;')
            self.HANG_SP.setStyleSheet('background-color: white;')
            self.HANG_LV.setStyleSheet('background-color: white;')

        else:
            self.HANG_DX.setDisabled(True)
            self.HANG_DY.setDisabled(True)
            self.HANG_DZ.setDisabled(True)
            self.HANG_SP.setDisabled(True)
            self.HANG_LV.setDisabled(True)
            self.HANG_DX.setStyleSheet('background-color: LightGray;')
            self.HANG_DY.setStyleSheet('background-color: LightGray;')
            self.HANG_DZ.setStyleSheet('background-color: LightGray;')
            self.HANG_SP.setStyleSheet('background-color: LightGray;')
            self.HANG_LV.setStyleSheet('background-color: LightGray;')
            self.HANG_DX.clear()
            self.HANG_DY.clear()
            self.HANG_DX.clear()
            self.HANG_SP.clear()
            self.HANG_LV.clear()
        # 第二部分
        if self.RSTN_2.isChecked():
            self.RSTN_DX_2.setDisabled(False)
            self.RSTN_DY_2.setDisabled(False)
            self.RSTN_DZ_2.setDisabled(False)
            self.RSTN_SP_2.setDisabled(False)
            self.RSTN_LV_2.setDisabled(False)
            self.RSTN_DX_2.setStyleSheet('background-color: white;')
            self.RSTN_DY_2.setStyleSheet('background-color: white;')
            self.RSTN_DZ_2.setStyleSheet('background-color: white;')
            self.RSTN_SP_2.setStyleSheet('background-color: white;')
            self.RSTN_LV_2.setStyleSheet('background-color: white;')

        else:
            self.RSTN_DX_2.setDisabled(True)
            self.RSTN_DY_2.setDisabled(True)
            self.RSTN_DZ_2.setDisabled(True)
            self.RSTN_SP_2.setDisabled(True)
            self.RSTN_LV_2.setDisabled(True)
            self.RSTN_DX_2.setStyleSheet('background-color: LightGray;')
            self.RSTN_DY_2.setStyleSheet('background-color: LightGray;')
            self.RSTN_DZ_2.setStyleSheet('background-color: LightGray;')
            self.RSTN_SP_2.setStyleSheet('background-color: LightGray;')
            self.RSTN_LV_2.setStyleSheet('background-color: LightGray;')
            self.RSTN_DX_2.clear()
            self.RSTN_DY_2.clear()
            self.RSTN_DX_2.clear()
            self.RSTN_SP_2.clear()
            self.RSTN_LV_2.clear()
        if self.SNUB_2.isChecked():
            self.SNUB_DX_2.setDisabled(False)
            self.SNUB_DY_2.setDisabled(False)
            self.SNUB_DZ_2.setDisabled(False)
            self.SNUB_SP_2.setDisabled(False)
            self.SNUB_LV_2.setDisabled(False)
            self.SNUB_DX_2.setStyleSheet('background-color: white;')
            self.SNUB_DY_2.setStyleSheet('background-color: white;')
            self.SNUB_DZ_2.setStyleSheet('background-color: white;')
            self.SNUB_SP_2.setStyleSheet('background-color: white;')
            self.SNUB_LV_2.setStyleSheet('background-color: white;')

        else:
            self.SNUB_DX_2.setDisabled(True)
            self.SNUB_DY_2.setDisabled(True)
            self.SNUB_DZ_2.setDisabled(True)
            self.SNUB_SP_2.setDisabled(True)
            self.SNUB_LV_2.setDisabled(True)
            self.SNUB_DX_2.setStyleSheet('background-color: LightGray;')
            self.SNUB_DY_2.setStyleSheet('background-color: LightGray;')
            self.SNUB_DZ_2.setStyleSheet('background-color: LightGray;')
            self.SNUB_SP_2.setStyleSheet('background-color: LightGray;')
            self.SNUB_LV_2.setStyleSheet('background-color: LightGray;')
            self.SNUB_DX_2.clear()
            self.SNUB_DY_2.clear()
            self.SNUB_DX_2.clear()
            self.SNUB_SP_2.clear()
            self.SNUB_LV_2.clear()

        if self.RSUP_2.isChecked():
            self.RSUP_DX_2.setDisabled(False)
            self.RSUP_DY_2.setDisabled(False)
            self.RSUP_DZ_2.setDisabled(False)
            self.RSUP_SP_2.setDisabled(False)
            self.RSUP_LV_2.setDisabled(False)
            self.RSUP_DX_2.setStyleSheet('background-color: white;')
            self.RSUP_DY_2.setStyleSheet('background-color: white;')
            self.RSUP_DZ_2.setStyleSheet('background-color: white;')
            self.RSUP_SP_2.setStyleSheet('background-color: white;')
            self.RSUP_LV_2.setStyleSheet('background-color: white;')

        else:
            self.RSUP_DX_2.setDisabled(True)
            self.RSUP_DY_2.setDisabled(True)
            self.RSUP_DZ_2.setDisabled(True)
            self.RSUP_SP_2.setDisabled(True)
            self.RSUP_LV_2.setDisabled(True)
            self.RSUP_DX_2.setStyleSheet('background-color: LightGray;')
            self.RSUP_DY_2.setStyleSheet('background-color: LightGray;')
            self.RSUP_DZ_2.setStyleSheet('background-color: LightGray;')
            self.RSUP_SP_2.setStyleSheet('background-color: LightGray;')
            self.RSUP_LV_2.setStyleSheet('background-color: LightGray;')
            self.RSUP_DX_2.clear()
            self.RSUP_DY_2.clear()
            self.RSUP_DX_2.clear()
            self.RSUP_SP_2.clear()
            self.RSUP_LV_2.clear()

        if self.HANG_2.isChecked():
            self.HANG_DX_2.setDisabled(False)
            self.HANG_DY_2.setDisabled(False)
            self.HANG_DZ_2.setDisabled(False)
            self.HANG_SP_2.setDisabled(False)
            self.HANG_LV_2.setDisabled(False)
            self.HANG_DX_2.setStyleSheet('background-color: white;')
            self.HANG_DY_2.setStyleSheet('background-color: white;')
            self.HANG_DZ_2.setStyleSheet('background-color: white;')
            self.HANG_SP_2.setStyleSheet('background-color: white;')
            self.HANG_LV_2.setStyleSheet('background-color: white;')

        else:
            self.HANG_DX_2.setDisabled(True)
            self.HANG_DY_2.setDisabled(True)
            self.HANG_DZ_2.setDisabled(True)
            self.HANG_SP_2.setDisabled(True)
            self.HANG_LV_2.setDisabled(True)
            self.HANG_DX_2.setStyleSheet('background-color: LightGray;')
            self.HANG_DY_2.setStyleSheet('background-color: LightGray;')
            self.HANG_DZ_2.setStyleSheet('background-color: LightGray;')
            self.HANG_SP_2.setStyleSheet('background-color: LightGray;')
            self.HANG_LV_2.setStyleSheet('background-color: LightGray;')
            self.HANG_DX_2.clear()
            self.HANG_DY_2.clear()
            self.HANG_DX_2.clear()
            self.HANG_SP_2.clear()
            self.HANG_LV_2.clear()

        # 第三部分
        if self.RSTN_3.isChecked():
            self.RSTN_DX_3.setDisabled(False)
            self.RSTN_DY_3.setDisabled(False)
            self.RSTN_DZ_3.setDisabled(False)
            self.RSTN_SP_3.setDisabled(False)
            self.RSTN_LV_3.setDisabled(False)
            self.RSTN_DX_3.setStyleSheet('background-color: white;')
            self.RSTN_DY_3.setStyleSheet('background-color: white;')
            self.RSTN_DZ_3.setStyleSheet('background-color: white;')
            self.RSTN_SP_3.setStyleSheet('background-color: white;')
            self.RSTN_LV_3.setStyleSheet('background-color: white;')

        else:
            self.RSTN_DX_3.setDisabled(True)
            self.RSTN_DY_3.setDisabled(True)
            self.RSTN_DZ_3.setDisabled(True)
            self.RSTN_SP_3.setDisabled(True)
            self.RSTN_LV_3.setDisabled(True)
            self.RSTN_DX_3.setStyleSheet('background-color: LightGray;')
            self.RSTN_DY_3.setStyleSheet('background-color: LightGray;')
            self.RSTN_DZ_3.setStyleSheet('background-color: LightGray;')
            self.RSTN_SP_3.setStyleSheet('background-color: LightGray;')
            self.RSTN_LV_3.setStyleSheet('background-color: LightGray;')
            self.RSTN_DX_3.clear()
            self.RSTN_DY_3.clear()
            self.RSTN_DX_3.clear()
            self.RSTN_SP_3.clear()
            self.RSTN_LV_3.clear()
        if self.SNUB_3.isChecked():
            self.SNUB_DX_3.setDisabled(False)
            self.SNUB_DY_3.setDisabled(False)
            self.SNUB_DZ_3.setDisabled(False)
            self.SNUB_SP_3.setDisabled(False)
            self.SNUB_LV_3.setDisabled(False)
            self.SNUB_DX_3.setStyleSheet('background-color: white;')
            self.SNUB_DY_3.setStyleSheet('background-color: white;')
            self.SNUB_DZ_3.setStyleSheet('background-color: white;')
            self.SNUB_SP_3.setStyleSheet('background-color: white;')
            self.SNUB_LV_3.setStyleSheet('background-color: white;')

        else:
            self.SNUB_DX_3.setDisabled(True)
            self.SNUB_DY_3.setDisabled(True)
            self.SNUB_DZ_3.setDisabled(True)
            self.SNUB_SP_3.setDisabled(True)
            self.SNUB_LV_3.setDisabled(True)
            self.SNUB_DX_3.setStyleSheet('background-color: LightGray;')
            self.SNUB_DY_3.setStyleSheet('background-color: LightGray;')
            self.SNUB_DZ_3.setStyleSheet('background-color: LightGray;')
            self.SNUB_SP_3.setStyleSheet('background-color: LightGray;')
            self.SNUB_LV_3.setStyleSheet('background-color: LightGray;')
            self.SNUB_DX_3.clear()
            self.SNUB_DY_3.clear()
            self.SNUB_DX_3.clear()
            self.SNUB_SP_3.clear()
            self.SNUB_LV_3.clear()

        if self.RSUP_3.isChecked():
            self.RSUP_DX_3.setDisabled(False)
            self.RSUP_DY_3.setDisabled(False)
            self.RSUP_DZ_3.setDisabled(False)
            self.RSUP_SP_3.setDisabled(False)
            self.RSUP_LV_3.setDisabled(False)
            self.RSUP_DX_3.setStyleSheet('background-color: white;')
            self.RSUP_DY_3.setStyleSheet('background-color: white;')
            self.RSUP_DZ_3.setStyleSheet('background-color: white;')
            self.RSUP_SP_3.setStyleSheet('background-color: white;')
            self.RSUP_LV_3.setStyleSheet('background-color: white;')

        else:
            self.RSUP_DX_3.setDisabled(True)
            self.RSUP_DY_3.setDisabled(True)
            self.RSUP_DZ_3.setDisabled(True)
            self.RSUP_SP_3.setDisabled(True)
            self.RSUP_LV_3.setDisabled(True)
            self.RSUP_DX_3.setStyleSheet('background-color: LightGray;')
            self.RSUP_DY_3.setStyleSheet('background-color: LightGray;')
            self.RSUP_DZ_3.setStyleSheet('background-color: LightGray;')
            self.RSUP_SP_3.setStyleSheet('background-color: LightGray;')
            self.RSUP_LV_3.setStyleSheet('background-color: LightGray;')
            self.RSUP_DX_3.clear()
            self.RSUP_DY_3.clear()
            self.RSUP_DX_3.clear()
            self.RSUP_SP_3.clear()
            self.RSUP_LV_3.clear()

        if self.HANG_3.isChecked():
            self.HANG_DX_3.setDisabled(False)
            self.HANG_DY_3.setDisabled(False)
            self.HANG_DZ_3.setDisabled(False)
            self.HANG_SP_3.setDisabled(False)
            self.HANG_LV_3.setDisabled(False)
            self.HANG_DX_3.setStyleSheet('background-color: white;')
            self.HANG_DY_3.setStyleSheet('background-color: white;')
            self.HANG_DZ_3.setStyleSheet('background-color: white;')
            self.HANG_SP_3.setStyleSheet('background-color: white;')
            self.HANG_LV_3.setStyleSheet('background-color: white;')

        else:
            self.HANG_DX_3.setDisabled(True)
            self.HANG_DY_3.setDisabled(True)
            self.HANG_DZ_3.setDisabled(True)
            self.HANG_SP_3.setDisabled(True)
            self.HANG_LV_3.setDisabled(True)
            self.HANG_DX_3.setStyleSheet('background-color: LightGray;')
            self.HANG_DY_3.setStyleSheet('background-color: LightGray;')
            self.HANG_DZ_3.setStyleSheet('background-color: LightGray;')
            self.HANG_SP_3.setStyleSheet('background-color: LightGray;')
            self.HANG_LV_3.setStyleSheet('background-color: LightGray;')
            self.HANG_DX_3.clear()
            self.HANG_DY_3.clear()
            self.HANG_DX_3.clear()
            self.HANG_SP_3.clear()
            self.HANG_LV_3.clear()
        # 第四部分
        if self.RSTN_4.isChecked():
            self.RSTN_DX_4.setDisabled(False)
            self.RSTN_DY_4.setDisabled(False)
            self.RSTN_DZ_4.setDisabled(False)
            self.RSTN_SP_4.setDisabled(False)
            self.RSTN_LV_4.setDisabled(False)
            self.RSTN_DX_4.setStyleSheet('background-color: white;')
            self.RSTN_DY_4.setStyleSheet('background-color: white;')
            self.RSTN_DZ_4.setStyleSheet('background-color: white;')
            self.RSTN_SP_4.setStyleSheet('background-color: white;')
            self.RSTN_LV_4.setStyleSheet('background-color: white;')

        else:
            self.RSTN_DX_4.setDisabled(True)
            self.RSTN_DY_4.setDisabled(True)
            self.RSTN_DZ_4.setDisabled(True)
            self.RSTN_SP_4.setDisabled(True)
            self.RSTN_LV_4.setDisabled(True)
            self.RSTN_DX_4.setStyleSheet('background-color: LightGray;')
            self.RSTN_DY_4.setStyleSheet('background-color: LightGray;')
            self.RSTN_DZ_4.setStyleSheet('background-color: LightGray;')
            self.RSTN_SP_4.setStyleSheet('background-color: LightGray;')
            self.RSTN_LV_4.setStyleSheet('background-color: LightGray;')
            self.RSTN_DX_4.clear()
            self.RSTN_DY_4.clear()
            self.RSTN_DX_4.clear()
            self.RSTN_SP_4.clear()
            self.RSTN_LV_4.clear()
        if self.SNUB_4.isChecked():
            self.SNUB_DX_4.setDisabled(False)
            self.SNUB_DY_4.setDisabled(False)
            self.SNUB_DZ_4.setDisabled(False)
            self.SNUB_SP_4.setDisabled(False)
            self.SNUB_LV_4.setDisabled(False)
            self.SNUB_DX_4.setStyleSheet('background-color: white;')
            self.SNUB_DY_4.setStyleSheet('background-color: white;')
            self.SNUB_DZ_4.setStyleSheet('background-color: white;')
            self.SNUB_SP_4.setStyleSheet('background-color: white;')
            self.SNUB_LV_4.setStyleSheet('background-color: white;')

        else:
            self.SNUB_DX_4.setDisabled(True)
            self.SNUB_DY_4.setDisabled(True)
            self.SNUB_DZ_4.setDisabled(True)
            self.SNUB_SP_4.setDisabled(True)
            self.SNUB_LV_4.setDisabled(True)
            self.SNUB_DX_4.setStyleSheet('background-color: LightGray;')
            self.SNUB_DY_4.setStyleSheet('background-color: LightGray;')
            self.SNUB_DZ_4.setStyleSheet('background-color: LightGray;')
            self.SNUB_SP_4.setStyleSheet('background-color: LightGray;')
            self.SNUB_LV_4.setStyleSheet('background-color: LightGray;')
            self.SNUB_DX_4.clear()
            self.SNUB_DY_4.clear()
            self.SNUB_DX_4.clear()
            self.SNUB_SP_4.clear()
            self.SNUB_LV_4.clear()

        if self.RSUP_4.isChecked():
            self.RSUP_DX_4.setDisabled(False)
            self.RSUP_DY_4.setDisabled(False)
            self.RSUP_DZ_4.setDisabled(False)
            self.RSUP_SP_4.setDisabled(False)
            self.RSUP_LV_4.setDisabled(False)
            self.RSUP_DX_4.setStyleSheet('background-color: white;')
            self.RSUP_DY_4.setStyleSheet('background-color: white;')
            self.RSUP_DZ_4.setStyleSheet('background-color: white;')
            self.RSUP_SP_4.setStyleSheet('background-color: white;')
            self.RSUP_LV_4.setStyleSheet('background-color: white;')

        else:
            self.RSUP_DX_4.setDisabled(True)
            self.RSUP_DY_4.setDisabled(True)
            self.RSUP_DZ_4.setDisabled(True)
            self.RSUP_SP_4.setDisabled(True)
            self.RSUP_LV_4.setDisabled(True)
            self.RSUP_DX_4.setStyleSheet('background-color: LightGray;')
            self.RSUP_DY_4.setStyleSheet('background-color: LightGray;')
            self.RSUP_DZ_4.setStyleSheet('background-color: LightGray;')
            self.RSUP_SP_4.setStyleSheet('background-color: LightGray;')
            self.RSUP_LV_4.setStyleSheet('background-color: LightGray;')
            self.RSUP_DX_4.clear()
            self.RSUP_DY_4.clear()
            self.RSUP_DX_4.clear()
            self.RSUP_SP_4.clear()
            self.RSUP_LV_4.clear()

        if self.HANG_4.isChecked():
            self.HANG_DX_4.setDisabled(False)
            self.HANG_DY_4.setDisabled(False)
            self.HANG_DZ_4.setDisabled(False)
            self.HANG_SP_4.setDisabled(False)
            self.HANG_LV_4.setDisabled(False)
            self.HANG_DX_4.setStyleSheet('background-color: white;')
            self.HANG_DY_4.setStyleSheet('background-color: white;')
            self.HANG_DZ_4.setStyleSheet('background-color: white;')
            self.HANG_SP_4.setStyleSheet('background-color: white;')
            self.HANG_LV_4.setStyleSheet('background-color: white;')

        else:
            self.HANG_DX_4.setDisabled(True)
            self.HANG_DY_4.setDisabled(True)
            self.HANG_DZ_4.setDisabled(True)
            self.HANG_SP_4.setDisabled(True)
            self.HANG_LV_4.setDisabled(True)
            self.HANG_DX_4.setStyleSheet('background-color: LightGray;')
            self.HANG_DY_4.setStyleSheet('background-color: LightGray;')
            self.HANG_DZ_4.setStyleSheet('background-color: LightGray;')
            self.HANG_SP_4.setStyleSheet('background-color: LightGray;')
            self.HANG_LV_4.setStyleSheet('background-color: LightGray;')
            self.HANG_DX_4.clear()
            self.HANG_DY_4.clear()
            self.HANG_DX_4.clear()
            self.HANG_SP_4.clear()
            self.HANG_LV_4.clear()

    def get_file_path(self):
        """
        获取配置文件下各种文件路径
        :return:
        """

        name = os.path.basename(self.data_path)
        fre_name = os.path.splitext(name)[0]
        self.fre_file_name = fre_name
        max_path = ''
        prr_path = ''
        ppo_path = ''
        prc_path = ''
        prd_path = ''
        dict_path = {'max': '', 'prr': '', 'ppo': '', 'prc': '', 'prd': ''}
        root, dirs, files = list(os.walk(os.path.dirname(self.data_path)))[0]
        for file in files:
            file_name = os.path.splitext(file)[0]
            if fre_name == file_name:
                if os.path.splitext(file)[1] == '.max':
                    data_max = os.path.join(root, file)
                    max_path = data_max
                    dict_path['max'] = max_path
                elif os.path.splitext(file)[1] == '.prr':
                    data_prr = os.path.join(root, file)
                    prr_path = data_prr
                    dict_path['prr'] = prr_path
                elif os.path.splitext(file)[1] == '.ppo':
                    data_ppo = os.path.join(root, file)
                    ppo_path = data_ppo
                    dict_path['ppo'] = ppo_path
                elif os.path.splitext(file)[1] == '.prc':  # 查找prc文件
                    data_prc = os.path.join(root, file)
                    prc_path = data_prc
                    dict_path['prc'] = prc_path
                elif os.path.splitext(file)[1] == '.prd':  # 查找prc文件
                    data_prd = os.path.join(root, file)
                    prd_path = data_prd
                    dict_path['prd'] = prd_path
        lack_file = ''
        for k in dict_path.keys():

            if not dict_path[k]:
                lack_file += k + ''

        if lack_file:
            print(lack_file)
            if 'max' in lack_file:
                QMessageBox.information(self, '提示', '缺少max文件，无法提取指定内容！')
                return False
            elif 'ppo' in lack_file:
                QMessageBox.information(self, '提示', '缺少ppo文件，无法提取支撑和设备接管载荷！')
            elif 'prr' in lack_file:
                QMessageBox.information(self, '提示', '缺少prr文件，无法提取阀门最大加速度！')
            elif 'prc' in lack_file:
                QMessageBox.information(self, '提示', '缺少prc文件，无法提取位移输出数据！')
            elif 'prd' in lack_file:
                QMessageBox.information(self, '提示', '缺少prd文件，无法提取位移输出数据！')
            return [max_path, prr_path, ppo_path, prc_path, prd_path]
        else:
            return [max_path, prr_path, ppo_path, prc_path, prd_path]

    def show_node(self):
        res1, res2 = self.show_node_end(self.lineEdit_4, self.textBrowser_5, self.textBrowser_7)
        return res1, res2

    def show_node3(self):
        res1, res2 = self.show_node_end(self.lineEdit_5, self.textBrowser_8, self.textBrowser_9)
        return res1, res2

    def show_node4(self):
        res1, res2 = self.show_node_end(self.lineEdit_10, self.textBrowser_10, self.textBrowser_11)
        return res1, res2

    def show_node5(self):
        res1, res2 = self.show_node_end(self.lineEdit_12, self.textBrowser_12, self.textBrowser_13)
        return res1, res2

    def show_node_end(self, widget1, widget2, widget3):
        """
        :param widget1: 待优化的支吊架节点
        :param widget2: 待优化支吊架类型和参数
        :param widget3: 支吊架可优化位置节点号
        :return:
        """
        try:
            if not self.data_path:
                QMessageBox.information(self, '提示', '请先配置fre文件')
                return None, None

            print("********")
            flag_line = ''
            old_node = widget1.text()
            old_node = self.analysis_num(old_node)  # 100  100,101,102   100 - 102 多种情况的输入

            if not old_node:
                old_node = []

            all_pt, all_pt1, hanger_line = self.get_pt_fre()  # 所有节点  所有绑定的节点  节点行数据

            # pt = 124
            options_node = all_pt - all_pt1  # 可操作的节点

            # old_node = all_pt1 & set(old_node)   # 需要在输入框中展示的节点编号

            # if not old_node:
            #     QMessageBox.information(self, '提示', "未找到指定的支架号！！！\n可优化支架号有" + str(all_pt1))

            print(old_node, "*****old_node*****")
            if old_node:
                widget1.setText(','.join(old_node) if len(old_node) > 1 else list(old_node)[0])  #

            message1 = ''
            print("**************")
            for node in old_node:
                # options_node.add(i)
                flag = 'PT=' + node + " "

                for j, line in enumerate(hanger_line):
                    if re.search(flag, line, re.IGNORECASE):
                        flag_line = flag_line + "*" + line

            widget2.setText(flag_line)

            options_node = self.all_set(options_node)
            if options_node:
                label_show = ','.join(options_node) if len(options_node) > 1 else options_node[0]
            else:
                label_show = ""
            widget3.setText(label_show)
            return True, flag_line

        except Exception as e:
            print(e)
            return None, None

    @staticmethod
    def all_set(all_s):
        """
        给节点号排序
        :param all_s: 可选节点号
        :return:
        """
        list1 = []
        list2 = []
        for j in all_s:
            try:
                list1.append(int(j))
            except ValueError:
                list2.append(j)
        list1.sort()
        list1 = [str(item) for item in list1]
        list2.sort()
        list1.extend(list2)
        return list1

    def show_node2(self):
        new_choice_node = self.show_node_end2(self.lineEdit_4, self.lineEdit_3)
        return new_choice_node

    def show_node9(self):
        new_choice_node = self.show_node_end2(self.lineEdit_5, self.lineEdit_9)
        return new_choice_node

    def show_node11(self):
        new_choice_node = self.show_node_end2(self.lineEdit_10, self.lineEdit_11)
        return new_choice_node

    def show_node13(self):
        new_choice_node = self.show_node_end2(self.lineEdit_12, self.lineEdit_13)
        return new_choice_node

    def show_node_end2(self, widget1, widget2):
        """拟优化位置节点号输入框编辑完成事件
        widget1: 待优化节点号输入框
        widget2: 拟优化节点号输入框
        """
        try:
            if not self.data_path:
                QMessageBox.information(self, '提示', "未配置.fre文件")
                return

            # message1 = ''
            # old_node = widget1.text()
            # old_node = self.analysis_num(old_node)

            new_node = widget2.text()
            new_node = self.analysis_num(new_node)

            all_pt, all_pt1, hanger_line = self.get_pt_fre()  # 所有节点  已绑定节点

            choice_pt = all_pt - all_pt1

            choice_pt = choice_pt & set(new_node)

            if not choice_pt:
                QMessageBox.information(self, '提示', "指定的节点号超出可优化位置范围")
                return None

            node_list = self.all_set(choice_pt)

            widget2.setText(','.join(node_list) if len(node_list) > 1 else node_list[0])
            return new_node
            # if new_node and old_node:
            #     for o in old_node:
            #         choice_pt.add(o)
            #
            #     for i in new_node:
            #         if str(i) not in choice_pt:
            #             message1 += str(i) + ','
            #     new_node = choice_pt & set(new_node)
            #     print(new_node)
            #     widget2.setText(','.join(new_node))
            #
            #     if message1 and not new_node:
            #         message1 += '节点超出可优化位置范围'
            #         QMessageBox.information(self, '提示', message1)
            #     return new_node

        except Exception as e:
            print(e)
            return None

    def button_get_result(self):
        """
        获取优化后的支吊架计算结果
        其中应力比按从小到大进行排序
        :return:
        """
        self.fre_less1 = ''
        self.stackedWidget.setCurrentIndex(5)
        if self.data_path:
            fre_dir = os.path.dirname(self.data_path)
            directory = QFileDialog.getExistingDirectory(None, "选取文件夹", fre_dir)  # 起始路径
        else:
            directory = QFileDialog.getExistingDirectory(None, "选取文件夹", "C:/")  # 起始路径
        if directory:
            self.listWidget_9.clear()
            self.listWidget_6.clear()
            self.textBrowser_6.clear()

            max_filename_list = []
            fre_filename_list = []

            # 递归每一个目录
            root, dirs, files = list(os.walk(directory))[0]
            for file in files:
                if os.path.splitext(file)[1] == '.max':
                    data_max = os.path.join(directory, file)
                    max_filename_list.append(data_max)
                if os.path.splitext(file)[1] == '.fre':
                    data_fre = os.path.join(directory, file)
                    fre_filename_list.append(data_fre)

            # 此处写原fre结果
            try:
                print(max_filename_list)
                if max_filename_list:
                    print(max_filename_list, "********max_list********")
                    self.data_dict, self.fre_less1, self.data_less1 = GetMaxResult(directory, max_filename_list,
                                                                                   self.max_path).get_max_files()
                    print(self.fre_less1)
                else:
                    QMessageBox.information(self, '提示', '缺少.max结果文件')
                #   self.data_dict, self.fre_less1, self.data_less1 = GetMaxResult(directory, max_filename_list, '').get_max_files()、

                if fre_filename_list:
                    self.fre_dict = GetFreResult(directory, fre_filename_list).get_fre_files()
                    print('来了吗但是', self.fre_dict)
                    self.set_listwidget_9(self.fre_dict)

                print('走到这里来了没')
                # 初始化所有方程应力比小于1 的item
                # self.fre_dict1 = GetFreResult(directory, self.fre_less1).get_fre_files()
                if self.fre_less1:
                    self.set_listwidget_6(self.fre_less1)
            except Exception as e:
                print(e, '错误出现')

    def get_hanger_data(self, item):
        """
        获取结果
        :return:
        """
        self.textBrowser_6.clear()
        # self.data_dict
        try:

            if item.text() in self.data_dict.keys():
                self.textBrowser_6.setText(self.data_dict[item.text()])

            else:
                QMessageBox.information(self, '提示', '支吊架未计算成功！')
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', '未能读到结果文件！或文件不存在')

    def get_hanger_data3(self, item):
        """
        获取吊架优化命令
        :return:
        """
        self.textBrowser_6.clear()

        try:

            if item.text() in self.fre_dict.keys():
                self.textBrowser_6.setText(self.fre_dict[item.text()])

            else:
                QMessageBox.information(self, '提示', '支吊架未计算成功！')

        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', '未能读到结果文件！或文件不存在')

    def get_hanger_data6(self, item):
        """
        获取应力比小于1的结果
        :return:
        """
        self.textBrowser_6.clear()
        try:
            if item.text() in self.fre_less1:
                self.textBrowser_6.setText(self.data_less1[item.text()])

            else:
                QMessageBox.information(self, '提示', '支吊架未计算成功！')

        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', '未能读到结果文件！或文件不存在')

    def button_gen_ref(self):
        """
        开始生成输入卡操作
        获取优化支吊架号
        读取fre中命令流
        :return:
        """
        try:
            flag_check = True
            flag1 = False
            flag2 = False

            if not self.data_path:
                QMessageBox.information(self, '提示', '请先配置fre文件路径！')
                return

            # 创建optimization文件夹
            new_fre_dir = os.path.join(os.path.dirname(self.data_path), 'optimization_%s' % self.dir_num)

            while os.path.exists(new_fre_dir):
                self.dir_num += 1
                new_fre_dir = os.path.join(os.path.dirname(self.data_path), 'optimization_%s' % self.dir_num)

            os.makedirs(new_fre_dir)

            file_number = 0
            insert_index = 0
            old_node_lines = []
            old_node_index = []
            self.max_file_list = {}
            self.fre_file_list = {}
            # 原支吊架节点号和现阶段支吊架节点号
            old_node = self.lineEdit_4.text()
            new_node = self.lineEdit_3.text()
            new_node = self.analysis_num(new_node)
            old_node = self.analysis_num(old_node)

            # 检查数据是否为空，个数是否正确，是否存在原

            flag1, res2 = self.show_node()
            flag2 = self.show_node2()

            if new_node and old_node and flag1 and flag2:
                all_node_comb = self.make_comb(old_node, new_node)  # 所有的，old -> new 的映射关系的列表
                exclude_reg = re.compile(
                    "(ANCH)|(NOZZ)|(CONN)|(CSUP)|(DSUP)|(MULR)|(NRSP)|(NRST)|(RSTN)|(SNUB)|(RSUP)|(HANG)|(VSUP)|(JUNC)|(GAPR)|(ROTR)",
                    re.IGNORECASE)
                for i in old_node:
                    flag = 'PT=' + str(i) + " "
                    with open(self.data_path, 'r', errors='ignore') as f:
                        lines = f.readlines()

                    for j, line in enumerate(lines):
                        m0 = re.search(flag, line, re.IGNORECASE)
                        if line.split():
                            if line.split()[0] and not line.startswith('*'):
                                m1 = exclude_reg.search(line.split()[0])
                                if m0 and m1:
                                    old_node_lines.append(line)
                                    old_node_index.append(j)
                        # 结尾标识
                        if 'ENDP' in line:
                            insert_index = j

                if not insert_index:
                    insert_index = old_node_index[-1] + 1

                # 删除掉以前的行数
                for i, item in enumerate(lines[:]):

                    for n in old_node_index:
                        if i == n:
                            lines.remove(item)

                # 删除行后，行的下标往前移动了，所有行号也要往前移动
                insert_index = insert_index - len(old_node_index)

                if self.RSTN.isChecked():
                    dx = self.analysis_num(self.RSTN_DX.text())
                    dy = self.analysis_num(self.RSTN_DY.text())
                    dz = self.analysis_num(self.RSTN_DZ.text())
                    sp = self.analysis_num3(self.RSTN_SP.text())
                    lv = self.RSTN_LV.text()

                    if not dx and not dy and not dz:
                        dx, dy, dz = ['0'], ['0'], ['0']
                    dx_list = self.get_hanger_one('DX', dx)
                    dy_list = self.get_hanger_one('DY', dy)
                    dz_list = self.get_hanger_one('DZ', dz)
                    sp_list = self.get_hanger_one('SP', sp)
                    if not sp_list:
                        sp_list = [('SP', None)]

                    rstn_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
                    data_lines = GenRefLines().get_new_lines(rstn_kinds, all_node_comb, 'RSTN', res2, lv)
                    print(data_lines)
                    file_number = self.write_into_fre(file_number, new_fre_dir, self.max_file_list,
                                                      self.fre_file_list, data_lines, insert_index, lines)

                if self.SNUB.isChecked():
                    dx = self.analysis_num(self.SNUB_DX.text())
                    dy = self.analysis_num(self.SNUB_DY.text())
                    dz = self.analysis_num(self.SNUB_DZ.text())
                    sp = self.analysis_num3(self.SNUB_SP.text())
                    lv = self.SNUB_LV.text()

                    if not dx and not dy and not dz:
                        dx, dy, dz = ['0'], ['0'], ['0']
                    dx_list = self.get_hanger_one('DX', dx)
                    dy_list = self.get_hanger_one('DY', dy)
                    dz_list = self.get_hanger_one('DZ', dz)
                    sp_list = self.get_hanger_one('SP', sp)
                    if not sp_list:
                        sp_list = [('SP', None)]
                    print(dx_list, dz_list, dy_list, sp_list)
                    snub_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
                    print(snub_kinds)
                    data_lines = GenRefLines().get_new_lines(snub_kinds, all_node_comb, 'SNUB', res2, lv)
                    file_number = self.write_into_fre(file_number, new_fre_dir, self.max_file_list,
                                                      self.fre_file_list, data_lines, insert_index, lines)

                if self.RSUP.isChecked():
                    dx = self.analysis_num(self.RSUP_DX.text())
                    dy = self.analysis_num(self.RSUP_DY.text())
                    dz = self.analysis_num(self.RSUP_DZ.text())
                    sp = self.analysis_num3(self.RSUP_SP.text())
                    lv = self.RSUP_LV.text()
                    if not dx and not dy and not dz:
                        dx, dy, dz = ['0'], ['0'], ['0']
                    dx_list = self.get_hanger_one('DX', dx)
                    dy_list = self.get_hanger_one('DY', dy)
                    dz_list = self.get_hanger_one('DZ', dz)
                    sp_list = self.get_hanger_one('SP', sp)
                    if not sp_list:
                        sp_list = [('SP', None)]
                    rsup_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
                    data_lines = GenRefLines().get_new_lines(rsup_kinds, all_node_comb, 'RSUP', res2, lv)
                    file_number = self.write_into_fre(file_number, new_fre_dir, self.max_file_list,
                                                      self.fre_file_list, data_lines, insert_index, lines)

                if self.HANG.isChecked():
                    dx = self.analysis_num(self.HANG_DX.text())
                    dy = self.analysis_num(self.HANG_DY.text())
                    dz = self.analysis_num(self.HANG_DZ.text())
                    sp = self.analysis_num3(self.HANG_SP.text())
                    lv = self.HANG_LV.text()
                    if not dx and not dy and not dz:
                        dx, dy, dz = ['0'], ['0'], ['0']
                    dx_list = self.get_hanger_one('DX', dx)
                    dy_list = self.get_hanger_one('DY', dy)
                    dz_list = self.get_hanger_one('DZ', dz)
                    sp_list = self.get_hanger_one('SP', sp)
                    if not sp_list:
                        sp_list = [('SP', None)]
                    hang_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
                    data_lines = GenRefLines().get_new_lines(hang_kinds, all_node_comb, 'HANG', res2, lv)
                    file_number = self.write_into_fre(file_number, new_fre_dir, self.max_file_list,
                                                      self.fre_file_list, data_lines, insert_index, lines)

                if not self.RSTN.isChecked() and not self.SNUB.isChecked() and not self.RSUP.isChecked() \
                        and not self.HANG.isChecked():
                    # 只优化节点号的工况
                    all_lines = []
                    for node_comb in all_node_comb:
                        print('*********************************')
                        new_line = self.change_node_only(old_node_lines, node_comb)
                        all_lines.append(new_line)
                    file_number = self.write_into_fre(file_number, new_fre_dir, self.max_file_list,
                                                      self.fre_file_list, all_lines,
                                                      insert_index, lines)

                show_path = new_fre_dir.replace('\\', '/')
                QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % show_path)

                # self.set_listwidget_9(self.fre_file_list)

            else:
                QMessageBox.information(self, '提示', '输入数据未填写完整')
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', str(e))

    def button_gen_ref2(self):
        """
        点击多个支吊架优化情况
        :return:
        """

        try:
            flag_check = True
            flag1 = False
            flag2 = False

            if not self.data_path:
                QMessageBox.information(self, '提示', '请先配置fre文件路径！')

            if self.data_path:
                # 创建optimization文件夹
                new_fre_dir = os.path.join(os.path.dirname(self.data_path), 'optimization_%s' % self.dir_num)

                if os.path.exists(new_fre_dir):
                    self.dir_num += 1
                    new_fre_dir = os.path.join(os.path.dirname(self.data_path), 'optimization_%s' % self.dir_num)
                    os.makedirs(new_fre_dir)

                else:
                    os.makedirs(new_fre_dir)

                # 第一步，先拿到所有的新 旧节点，排列组合，筛选出重复的。 删除老的节点，形成新的lines
                # 第二步，分别获取第1个优化以及2个优化3个优化返回的对应的新节点的 所有情况，得到hanger1\hanger2\hanger3 3个字典
                # 将每个字典的行根据DX，DZ，DY不同，形成写入的行
                # 第三步，遍历所有的情况，分别从hanger1、hanger2\ hanger3\ 中找到对应的节点对应的所有项的行，最后三个行相加
                # 返回的所有行最后有多少种情况，就写入到不同的文件里，放在同一个文件夹下面
                file_number = 0
                # insert_index = 0
                # old_node_lines = []
                # old_node_index = []
                # self.max_file_list = {}
                # self.fre_file_list = {}
                # 原支吊架节点号和现阶段支吊架节点号
                old_node1 = self.lineEdit_5.text()
                old_node2 = self.lineEdit_10.text()
                old_node3 = self.lineEdit_12.text()

                new_node1 = self.lineEdit_9.text()
                new_node2 = self.lineEdit_11.text()
                new_node3 = self.lineEdit_13.text()
                if old_node1:
                    old_node1 = self.analysis_num(old_node1)
                if old_node2:
                    old_node2 = self.analysis_num(old_node2)
                if old_node3:
                    old_node3 = self.analysis_num(old_node3)
                if new_node1:
                    new_node1 = self.analysis_num(new_node1)
                if new_node2:
                    new_node2 = self.analysis_num(new_node2)
                if new_node3:
                    new_node3 = self.analysis_num(new_node3)

                comb1, comb2, comb3 = [], [], []
                total_nodes = []
                # 删除的节点
                remove_nodes = []
                if old_node1 and new_node1:
                    comb1 = self.make_comb(old_node1, new_node1)
                    remove_nodes.extend(old_node1)
                if old_node2 and new_node2:
                    comb2 = self.make_comb(old_node2, new_node2)
                    remove_nodes.extend(old_node2)
                if old_node3 and new_node3:
                    comb3 = self.make_comb(old_node3, new_node3)
                    remove_nodes.extend(old_node3)
                old_nodes = list(set(remove_nodes))
                if len(old_nodes) < len(remove_nodes):
                    QMessageBox.information(self, '提示', '待优化号重复了')
                    return False
                old_lines, insert_index, flag_line, old_node_lines = self.remove_old_node(old_nodes)
                print(insert_index)

                if comb1 and comb2 and not comb3:
                    hangers = self.get_hanger_more(comb1, comb2)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization1(new_node1, old_node_lines, comb1)

                    all_lines2 = self.get_optimization2(new_node2, old_node_lines, comb2)
                    if all_lines1 and all_lines2:
                        total_lines = self.write_into_fre_file(total_nodes, all_lines1, all_lines2, flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)

                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)

                elif comb1 and comb3 and not comb2:
                    hangers = self.get_hanger_more(comb1, comb3)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization1(new_node1, old_node_lines, comb1)
                    all_lines2 = self.get_optimization3(new_node3, old_node_lines, comb3)
                    if all_lines1 and all_lines2:
                        total_lines = self.write_into_fre_file(total_nodes, all_lines1, all_lines2, flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)
                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)
                elif comb2 and comb3 and not comb1:
                    hangers = self.get_hanger_more(comb2, comb3)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization2(new_node2, old_node_lines, comb2)
                    all_lines2 = self.get_optimization3(new_node3, old_node_lines, comb3)
                    if all_lines1 and all_lines2:
                        total_lines = self.write_into_fre_file(total_nodes, all_lines1, all_lines2, flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)
                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)
                elif not comb2 and not comb1 and not comb3:
                    QMessageBox.information(self, '提示', '未填入数据')
                    return False
                elif comb1 and not comb2 and not comb3:
                    hangers = self.get_hanger_more(comb1)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization1(new_node1, old_node_lines, comb1)
                    print('hello', all_lines1)
                    if all_lines1:
                        total_lines = self.write_into_fre_file1(total_nodes, all_lines1, flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)
                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)
                elif comb2 and not comb1 and not comb3:
                    hangers = self.get_hanger_more(comb2)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization2(new_node2, old_node_lines, comb2)
                    if all_lines1:
                        total_lines = self.write_into_fre_file1(total_nodes, all_lines1, flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)
                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)

                elif comb3 and not comb1 and not comb2:
                    hangers = self.get_hanger_more(comb3)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization3(new_node3, old_node_lines, comb3)
                    if all_lines1:
                        total_lines = self.write_into_fre_file1(total_nodes, all_lines1, flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)
                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)
                elif comb1 and comb2 and comb3:
                    hangers = self.get_hanger_more(comb1, comb2, comb3)
                    total_nodes = self.remove_duplicates(hangers)
                    all_lines1 = self.get_optimization1(new_node1, old_node_lines, comb1)
                    all_lines2 = self.get_optimization2(new_node2, old_node_lines, comb2)
                    all_lines3 = self.get_optimization3(new_node3, old_node_lines, comb3)
                    if all_lines1 and all_lines2 and all_lines3:
                        total_lines = self.write_into_fre_file3(total_nodes, all_lines1, all_lines2, all_lines3,
                                                                flag_line)
                        self.write_into_fre2(file_number, new_fre_dir, total_lines, insert_index, old_lines)
                        QMessageBox.information(self, '提示', '输入卡生成完毕！\n位置%s' % new_fre_dir)

        except Exception as e:

            QMessageBox.information(self, '提示', '数据未填写完整')

    @staticmethod
    def write_into_fre_file(key_node, dict1, dict2, old_line):
        """
        将生成的新行加入到原来的fre文件中去
        :param key_node:
        :param dict1:
        :param dict2:
        :param old_line:
        :return:
        """
        all_lines = []
        for item in key_node:
            a, b = item[0], item[1]
            for x in dict1[a]:
                for y in dict2[b]:
                    new_lines1 = '*********原支吊架参数命令流*************' + '\n'
                    new_lines1 += old_line
                    new_lines = '\n' + '*********优化后支吊架参数命令流**********' + '\n'
                    new_lines1 += new_lines
                    # new_line = '*********optimization***********' + '\n'
                    new_lines1 += x + y
                    all_lines.append(new_lines1)
        return all_lines

    @staticmethod
    def write_into_fre_file1(key_node, dict1, old_line):
        # 1种情况
        all_lines = []
        for item in key_node:
            a = item[0]
            for x in dict1[a]:
                new_lines1 = '*********原支吊架参数命令流*************' + '\n'
                new_lines1 += old_line
                new_lines = '\n' + '*********优化后支吊架参数命令流**********' + '\n'
                new_lines1 += new_lines
                # new_line = '*********optimization***********' + '\n'
                new_lines1 += x
                all_lines.append(new_lines1)
        return all_lines

    @staticmethod
    def write_into_fre_file3(key_node, dict1, dict2, dict3, old_line):
        # 1种情况
        all_lines = []
        for item in key_node:
            a, b, c = item[0], item[1], item[2]
            for x in dict1[a]:
                for y in dict2[b]:
                    for z in dict3[c]:
                        new_lines1 = '*********原支吊架参数命令流*************' + '\n'
                        new_lines1 += old_line
                        new_lines = '\n' + '*********优化后支吊架参数命令流**********' + '\n'
                        new_lines1 += new_lines
                        # new_line = '*********optimization***********' + '\n'
                        new_lines1 += x + y + z
                        all_lines.append(new_lines1)
        return all_lines

    def get_optimization2(self, new_pt, flag_line, all_node_comb):
        """
        获取第1个优化模块
        :return:
        """
        all_lines_pt = {}
        for i in new_pt:
            all_lines_pt[i] = []

        if self.RSTN_3.isChecked():

            dx = self.analysis_num(self.RSTN_DX_3.text())
            dy = self.analysis_num(self.RSTN_DY_3.text())
            dz = self.analysis_num(self.RSTN_DZ_3.text())
            sp = self.analysis_num3(self.RSTN_SP_3.text())
            lv = self.RSTN_LV_3.text()

            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]

            rstn_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            print(rstn_kinds)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, rstn_kinds, new_pt, 'RSTN', lv)

        if self.SNUB_3.isChecked():
            dx = self.analysis_num(self.SNUB_DX_3.text())
            dy = self.analysis_num(self.SNUB_DY_3.text())
            dz = self.analysis_num(self.SNUB_DZ_3.text())
            sp = self.analysis_num3(self.SNUB_SP_3.text())
            lv = self.SNUB_LV_3.text()

            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]

            snub_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            print(snub_kinds)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, snub_kinds, new_pt, 'SNUB', lv)

        if self.RSUP_3.isChecked():
            dx = self.analysis_num(self.RSUP_DX_3.text())
            dy = self.analysis_num(self.RSUP_DY_3.text())
            dz = self.analysis_num(self.RSUP_DZ_3.text())
            sp = self.analysis_num3(self.RSUP_SP_3.text())
            lv = self.RSUP_LV_3.text()
            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]
            rsup_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, rsup_kinds, new_pt, 'RSUP', lv)
            # file_number = self.write_into_fre(file_number, new_fre_dir, self.max_file_list,
            #                                   self.fre_file_list, data_lines, insert_index, lines)

        if self.HANG_3.isChecked():
            dx = self.analysis_num(self.HANG_DX_3.text())
            dy = self.analysis_num(self.HANG_DY_3.text())
            dz = self.analysis_num(self.HANG_DZ_3.text())
            sp = self.analysis_num3(self.HANG_SP_3.text())
            lv = self.HANG_LV_3.text()
            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]
            hang_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, hang_kinds, new_pt, 'HANG', lv)

        if not self.RSTN_3.isChecked() and not self.SNUB_3.isChecked() and not self.RSUP_3.isChecked() \
                and not self.HANG_3.isChecked():
            # 只优化节点号的工况
            # QMessageBox.information(self, '提示', '支吊架类型和参数未选择')
            # return None
            for node_comb in all_node_comb:
                new_line = self.change_node_only_one(flag_line, node_comb)
                for k, v in node_comb.items():
                    all_lines_pt[v].append(new_line)

        return all_lines_pt

    def get_optimization3(self, new_pt, flag_line, all_node_comb):
        """
        获取第1个优化模块
        :return:
        """
        all_lines_pt = {}
        for i in new_pt:
            all_lines_pt[i] = []

        if self.RSTN_4.isChecked():

            dx = self.analysis_num(self.RSTN_DX_4.text())
            dy = self.analysis_num(self.RSTN_DY_4.text())
            dz = self.analysis_num(self.RSTN_DZ_4.text())
            sp = self.analysis_num3(self.RSTN_SP_4.text())
            lv = self.RSTN_LV_4.text()

            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]

            rstn_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            print(rstn_kinds)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, rstn_kinds, new_pt, 'RSTN', lv)

        if self.SNUB_4.isChecked():
            dx = self.analysis_num(self.SNUB_DX_4.text())
            dy = self.analysis_num(self.SNUB_DY_4.text())
            dz = self.analysis_num(self.SNUB_DZ_4.text())
            sp = self.analysis_num3(self.SNUB_SP_4.text())
            lv = self.SNUB_LV_4.text()

            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]

            snub_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            print(snub_kinds)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, snub_kinds, new_pt, 'SNUB', lv)

        if self.RSUP_4.isChecked():
            dx = self.analysis_num(self.RSUP_DX_4.text())
            dy = self.analysis_num(self.RSUP_DY_4.text())
            dz = self.analysis_num(self.RSUP_DZ_4.text())
            sp = self.analysis_num3(self.RSUP_SP_4.text())
            lv = self.RSUP_LV_4.text()
            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]
            rsup_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, rsup_kinds, new_pt, 'RSUP', lv)

        if self.HANG_4.isChecked():
            dx = self.analysis_num(self.HANG_DX_4.text())
            dy = self.analysis_num(self.HANG_DY_4.text())
            dz = self.analysis_num(self.HANG_DZ_4.text())
            sp = self.analysis_num3(self.HANG_SP_4.text())
            lv = self.HANG_LV_4.text()
            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]
            hang_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, hang_kinds, new_pt, 'HANG', lv)

        if not self.RSTN_4.isChecked() and not self.SNUB_4.isChecked() and not self.RSUP_4.isChecked() \
                and not self.HANG_4.isChecked():
            # 只优化节点号的工况
            # QMessageBox.information(self, '提示', '支吊架类型和参数未选择')
            # return None
            for node_comb in all_node_comb:
                new_line = self.change_node_only_one(flag_line, node_comb)
                for k, v in node_comb.items():
                    all_lines_pt[v].append(new_line)

        return all_lines_pt

    def get_optimization1(self, new_pt, flag_line, all_node_comb):
        """
        flag_line, all_node_comb
        获取第1个优化模块
        :return:
        """
        all_lines_pt = {}
        for i in new_pt:
            all_lines_pt[i] = []

        if self.RSTN_2.isChecked():

            dx = self.analysis_num(self.RSTN_DX_2.text())
            dy = self.analysis_num(self.RSTN_DY_2.text())
            dz = self.analysis_num(self.RSTN_DZ_2.text())
            sp = self.analysis_num3(self.RSTN_SP_2.text())
            lv = self.RSTN_LV_2.text()

            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]

            rstn_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            print(rstn_kinds)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, rstn_kinds, new_pt, 'RSTN', lv)

        if self.SNUB_2.isChecked():
            dx = self.analysis_num(self.SNUB_DX_2.text())
            dy = self.analysis_num(self.SNUB_DY_2.text())
            dz = self.analysis_num(self.SNUB_DZ_2.text())
            sp = self.analysis_num3(self.SNUB_SP_2.text())
            lv = self.SNUB_LV_2.text()

            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]

            snub_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            print(snub_kinds)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, snub_kinds, new_pt, 'SNUB', lv)

        if self.RSUP_2.isChecked():
            dx = self.analysis_num(self.RSUP_DX_2.text())
            dy = self.analysis_num(self.RSUP_DY_2.text())
            dz = self.analysis_num(self.RSUP_DZ_2.text())
            sp = self.analysis_num3(self.RSUP_SP_2.text())
            lv = self.RSUP_LV_2.text()
            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]
            rsup_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, rsup_kinds, new_pt, 'RSUP', lv)

        if self.HANG_2.isChecked():
            dx = self.analysis_num(self.HANG_DX_2.text())
            dy = self.analysis_num(self.HANG_DY_2.text())
            dz = self.analysis_num(self.HANG_DZ_2.text())
            sp = self.analysis_num3(self.HANG_SP_2.text())
            lv = self.HANG_LV_2.text()
            if not dx and not dy and not dz:
                dx, dy, dz = ['0'], ['0'], ['0']
            dx_list = self.get_hanger_one('DX', dx)
            dy_list = self.get_hanger_one('DY', dy)
            dz_list = self.get_hanger_one('DZ', dz)
            sp_list = self.get_hanger_one('SP', sp)
            if not sp_list:
                sp_list = [('SP', None)]
            hang_kinds = self.get_hanger_all(dx_list, dy_list, dz_list, sp_list)
            data_lines = GenRefLines().get_new_lines_more(all_lines_pt, hang_kinds, new_pt, 'HANG', lv)

        if not self.RSTN_2.isChecked() and not self.SNUB_2.isChecked() and not self.RSUP_2.isChecked() \
                and not self.HANG_2.isChecked():
            # 只优化节点号的工况
            # QMessageBox.information(self, '提示', '支吊架类型和参数未选择')
            # return None
            for node_comb in all_node_comb:
                new_line = self.change_node_only_one(flag_line, node_comb)
                for k, v in node_comb.items():
                    all_lines_pt[v].append(new_line)

        return all_lines_pt

    def remove_old_node(self, old_node):
        """
        删除以前的节点号,重新生成新的文件
        在生成新的行后写入文件末尾
        :param old_node: 老节点
        :return:删除老节点后的剩余行,新行插入下标,被删除的行
        """
        flag_line = ''
        insert_index = 0
        old_node_lines = []
        old_node_index = []
        exclude_reg = re.compile(
            "(ANCH)|(NOZZ)|(CONN)|(CSUP)|(DSUP)|(MULR)|(NRSP)|(NRST)|(RSTN)|(SNUB)|(RSUP)|(HANG)|(VSUP)|(JUNC)|(GAPR)|(ROTR)",
            re.IGNORECASE)
        for i in old_node:
            # 遍历老节点
            flag = 'PT=' + str(i) + " "
            with open(self.data_path, 'r', errors='ignore') as f:
                lines = f.readlines()

            for j, line in enumerate(lines):
                m0 = re.search(flag, line, re.IGNORECASE)
                if line.split():
                    if line.split()[0] and not line.startswith('*'):
                        m1 = exclude_reg.search(line.split()[0])
                        # m1 = re.search('RSTN', line.split()[0], re.IGNORECASE)
                        # m2 = re.search('SNUB', line.split()[0], re.IGNORECASE)
                        # m3 = re.search('RSUP', line.split()[0], re.IGNORECASE)
                        # m4 = re.search('HANG', line.split()[0], re.IGNORECASE)
                        if m0 and m1:
                            flag_line += '*' + line
                            old_node_lines.append(line)
                            old_node_index.append(j)
                if 'ENDP' in line:
                    insert_index = j

        if not insert_index:
            insert_index = old_node_index[-1] + 1

        # 删除掉以前的行数
        for i, item in enumerate(lines[:]):

            for n in old_node_index:
                if i == n:
                    lines.remove(item)

        # 删除行后，行的下标往前移动了，所有行号也要往前移动
        insert_index = insert_index - len(old_node_index)
        return lines, insert_index, flag_line, old_node_lines

    def set_listwidget_9(self, fre_dict):
        """
        设置listwidget_9
        :param fre_dict: fre文件列表
        :return:
        """
        self.listWidget_9.clear()
        print(fre_dict)
        ak = list(fre_dict.keys())
        ak.sort(key=lambda x: int(x.rsplit('_')[-1]))
        for fre_file in ak:
            item = QListWidgetItem()
            item.setText(fre_file)
            self.listWidget_9.addItem(item)

    def set_listwidget_6(self, fre_less_list):
        """
        设置listwidget_6
        :param fre_less_list: fre文件列表
        :return:
        """
        self.listWidget_6.clear()
        fre_less_list.sort(key=lambda x: int(x.rsplit('_')[-1]))
        for fre_file in fre_less_list:
            item = QListWidgetItem()
            item.setText(fre_file)
            self.listWidget_6.addItem(item)

    @staticmethod
    def change_node_only(old_lines, node_comb):
        """
        只考虑更换节点号的情况
        :param old_lines: [RSTN PT=154 DX=0 DY=0 DZ=1  SP=25, SNUB PT=145 DX=0 DY=1 DZ=0]
        :param node_comb: {'154': 150, '139':'155'}
        :return:
        """
        new_line = '*********原支吊架参数命令流*************' + '\n'
        new_line += ('*' + '*'.join(old_lines))
        new_line += '\n' + '*********优化后支吊架参数命令流**********' + '\n'

        # new_line = '*********optimization***********' + '\n'
        for old_line in old_lines:
            for k, v in node_comb.items():
                old_pt = 'PT=' + k + " "
                if re.search(old_pt, old_line, re.IGNORECASE):
                    new_pt = 'PT=' + v + " "
                    # res = old_line.replace(old_pt, new_pt)
                    res = re.sub(old_pt, new_pt, old_line, flags=re.IGNORECASE)
                    new_line += res
        return new_line

    @staticmethod
    def change_node_only_one(old_lines, node_comb):
        """
        只考虑更换节点号的情况
        :param old_lines: [RSTN PT=154 DX=0 DY=0 DZ=1  SP=25, SNUB PT=145 DX=0 DY=1 DZ=0]
        :param node_comb: {'154': 150, '139':'155'}
        :return:
        """
        new_line = ''

        # new_line = '*********optimization***********' + '\n'
        print(old_lines)
        for old_line in old_lines:
            print(node_comb)
            for k, v in node_comb.items():
                print(111111)
                old_pt = 'PT=' + k + " "
                if re.search(old_pt, old_line, re.IGNORECASE):
                    new_pt = 'PT=' + v + " "
                    res = re.sub(old_pt, new_pt, old_line, flags=re.IGNORECASE)
                    new_line += res
        return new_line

    def clean_quote(self, line):
        """去掉注释，以最开始的*为标志"""
        line = line.strip()
        end_index = None
        for index, char in enumerate(line):
            if char == "*":
                end_index = index
                break

        return line[0:end_index]

    def get_pt_fre(self):
        """
        读取PT号，在fre文件中进行搜索
        :return:
        """
        all_pts = set()  # 记录所有节点
        # support_pts = set()  # 记录支撑的节点
        exclude_pts = set()  # 记录不能被添加支撑的节点
        flag_line = []  # 记录不能被添加的卡片 的行数据

        with open(self.data_path, 'r', errors='ignore') as f:
            lines = f.readlines()
        flag = r"PT=(\d+)"
        pt_reg = re.compile(flag, re.IGNORECASE)
        # support_reg = re.compile('(RSTN)|(SNUB)|(RSUP)|(HANG)', re.IGNORECASE)

        exclude_reg = re.compile(
            "(ANCH)|(NOZZ)|(CONN)|(CSUP)|(DSUP)|(MULR)|(NRSP)|(NRST)|(RSTN)|(SNUB)|(RSUP)|(HANG)|(VSUP)|(JUNC)|(GAPR)|(ROTR)",
            re.IGNORECASE)

        for line in lines:
            # 去掉注释
            line = self.clean_quote(line).strip() + "\n"
            if not line:
                continue

            # 是否是节点
            is_pt = pt_reg.search(line)
            if not is_pt:
                continue

            all_pts.add(is_pt.groups()[0])

            # 该节点是否有支撑
            # is_support = support_reg.search(line)
            # if is_support:
            #     flag_line.append(line)  # 记录该行数据
            #     support_pts.add(is_pt.groups()[0])
            #     all_pts.add(is_pt.groups()[0])

            is_exclude = exclude_reg.search(line)
            if is_exclude:  # 记录所有排除的行
                flag_line.append(line)  # 记录该行数据
                exclude_pts.add(is_pt.groups()[0])

        # all_pts = all_pts - exclude_pts

        return all_pts, exclude_pts, flag_line

    def write_into_fre(self, file_number, new_fre_dir, max_file_list, fre_file_list, data_lines, write_index,
                       old_lines):

        """
        将生成的文件写入新的文件当中
        :param file_number: 文件号
        :param new_fre_dir: 文件夹
        :param max_file_list: 文件名列表
        :param fre_file_list: 文件名列表
        :param data_lines: 所有情况的
        :param write_index: 写入位置
        :param old_lines: 删除标志后的行
        :return:
        """

        for user_line in data_lines:
            new_lines = old_lines[:]
            file_number += 1
            new_max_file = 'filename_%s.max' % file_number
            new_fre_file = '%s_%s.fre' % (self.fre_file_name, file_number)
            max_name = os.path.splitext(new_max_file)[0]
            fre_name = os.path.splitext(new_fre_file)[0]
            max_file_list[max_name] = user_line
            fre_file_list[fre_name] = user_line
            new_fre_file = os.path.join(new_fre_dir, new_fre_file)
            new_lines.insert(write_index, user_line)
            with open(new_fre_file, 'w', encoding='utf8', errors='ignore') as f:
                f.writelines(new_lines)
            del new_lines
        return file_number

    def write_into_fre2(self, file_number, new_fre_dir, data_lines, write_index, old_lines):

        """
        将生成的文件写入新的文件当中
        :param file_number: 文件号
        :param new_fre_dir: 文件夹
        :param max_file_list: 文件名列表
        :param fre_file_list: 文件名列表
        :param data_lines: 所有情况的
        :param write_index: 写入位置
        :param old_lines: 删除标志后的行
        :return:
        """

        for user_line in data_lines:
            new_lines = old_lines[:]
            file_number += 1
            new_max_file = 'filename_%s.max' % file_number
            new_fre_file = '%s_%s.fre' % (self.fre_file_name, file_number)
            # max_name = os.path.splitext(new_max_file)[0]
            # fre_name = os.path.splitext(new_fre_file)[0]
            # max_file_list[max_name] = user_line
            # fre_file_list[fre_name] = user_line
            new_fre_file = os.path.join(new_fre_dir, new_fre_file)
            new_lines.insert(write_index, user_line)
            with open(new_fre_file, 'w', encoding='utf8', errors='ignore') as f:
                f.writelines(new_lines)
            del new_lines
        return file_number

    @staticmethod
    def remove_duplicates(node_list):
        """
        去掉重复的
        :param list2:
        :return:
        """
        data_dict = []
        for item in node_list:
            d1 = []
            for i, j in enumerate(item):
                for k, v in j.items():
                    d1.append(v)
            data_dict.append(d1)
        for z in data_dict[:]:
            if len(set(z)) < len(z):
                data_dict.remove(z)
        return data_dict

    @staticmethod
    def get_hanger_more(*args):
        """
        从两个列表中获取组合
        :param hanger_data:节点号
        :param k: 关键字，key—name
        :return: [(k,1),(k,2),(k,3)]
        """
        hanger_parameters = []

        for h in itertools.product(*args):
            hanger_parameters.append(h)

        return hanger_parameters

    @staticmethod
    def get_hanger_one(k, hanger_data):
        """
        从两个列表中获取组合
        :param hanger_data:节点号
        :param k: 关键字，key—name
        :return: [(k,1),(k,2),(k,3)]
        """
        if hanger_data is None:
            hanger_data = [None]
        hanger_parameters = []
        for h in itertools.product([k], hanger_data):
            hanger_parameters.append(h)

        return hanger_parameters

    @staticmethod
    def get_hanger_all(*args):
        total_list = []
        for w in itertools.product(*args):  # 全部组合
            new_w = list(w)
            for x in w:
                if x[1] is None:
                    new_w.remove(x)
            new_d = dict(new_w)
            total_list.append(new_d)
        return total_list

    @staticmethod
    def make_comb(list1, list2):

        list1_tuple = tuple(list1)

        results = []
        for tmp_list in itertools.permutations(list2, len(list1)):
            results.append(dict(zip(list1_tuple, tmp_list)))

        return results

    @staticmethod
    def analysis_node_line(line):
        """
        解析字符串，TANG PT=26 EW=0 DZ=0.255
        :param line:
        :return: 返回一个字典
        """
        node_var = {}
        paras = line.strip().split()

        for i in paras:
            if '=' in i:
                v1, v2 = i.split('=')
                node_var[v1] = v2
            else:
                node_var[i] = ''

        return node_var

    def analysis_num(self, node_str):
        """
        解析数据
        :param node_str: 解析的字符串数据     1.100      2.101,102...     3.101-123，   123-102     4.多种组合 ，或, 分割
        :return:
        """

        try:
            nums = []
            if node_str:
                if ',' in node_str and '，' not in node_str:
                    nodes = node_str.split(',')
                    for node in nodes:
                        if '-' in node and node:
                            a, b = node.split('-')
                            if a and b:
                                n1 = int(a)
                                n2 = int(b)
                                n3 = int(a)
                                n4 = int(b)
                                if n1 < n2:
                                    while n1 <= n2:
                                        nums.append(str(n1))
                                        n1 += 1
                                if n3 > n4:
                                    while n3 >= n4:
                                        nums.append(str(n4))
                                        n4 += 1

                        else:
                            if node:
                                nums.append(node)
                elif '，' in node_str and ',' not in node_str:
                    nodes = node_str.split('，')
                    for node in nodes:
                        if '-' in node and node:
                            a, b = node.split('-')
                            if a and b:
                                n1 = int(a)
                                n2 = int(b)
                                n3 = int(a)
                                n4 = int(b)

                                if n1 < n2:
                                    while n1 <= n2:
                                        nums.append(str(n1))
                                        n1 += 1
                                if n3 > n4:
                                    while n3 >= n4:
                                        nums.append(str(n4))
                                        n4 += 1

                        else:
                            if node:
                                nums.append(node)
                elif ',' in node_str and '，' in node_str:
                    nodes = node_str.split(',')

                    # ['124，110-113', '123-125']
                    for node in nodes:
                        if '，' in node and node:
                            node1 = node.split('，')

                            # ['124', '110-113']
                            for node2 in node1:
                                if '-' in node2 and node2:
                                    a, b = node2.split('-')
                                    if a and b:
                                        n1 = int(a)
                                        n2 = int(b)
                                        n3 = int(a)
                                        n4 = int(b)

                                        if n1 < n2:
                                            while n1 <= n2:
                                                nums.append(str(n1))

                                                n1 += 1

                                        if n3 > n4:

                                            while n3 >= n4:
                                                nums.append(str(n4))
                                                n4 += 1
                                else:
                                    if node2:
                                        nums.append(node2)

                        if '-' in node and '，' not in node:
                            a, b = node.split('-')
                            if a and b:
                                n1 = int(a)
                                n2 = int(b)
                                n3 = int(a)
                                n4 = int(b)
                                if n1 < n2:
                                    while n1 <= n2:
                                        nums.append(str(n1))
                                        n1 += 1
                                if n3 > n4:
                                    while n3 >= n4:
                                        nums.append(str(n4))
                                        n4 += 1
                elif '-' in node_str and ',' not in node_str and '，' not in node_str:

                    a, b = node_str.split('-')
                    if a and b:
                        n1 = int(a)
                        n2 = int(b)
                        n3 = int(a)
                        n4 = int(b)
                        if n1 < n2:
                            while n1 <= n2:
                                nums.append(str(n1))
                                n1 += 1
                        if n3 > n4:
                            while n3 >= n4:
                                nums.append(str(n4))
                                n4 += 1
                else:
                    if node_str:
                        nums.append(node_str)
                if nums:
                    return list(set(nums))
                else:
                    QMessageBox.information(self, '提示', '输入格式不正确，请重新输入')
                    return False
        except Exception as e:
            QMessageBox.information(self, '提示', '输入格式不正确，请重新输入')
            return False

    @staticmethod
    def analysis_num3(node_str):

        pat = r'\d+\.\d+|\d+'
        all_dict = re.findall(pat, node_str)
        if all_dict:
            result = [i for i in all_dict if i]
            return result
        else:
            return []

    def button_data_click(self):

        fre_dir = get_default_path("fre_dir")

        name, _ = QFileDialog.getOpenFileName(self, '选择fre数据文件', fre_dir, '数据文件(*.fre *.fre)')
        if name:
            set_default_path("fre_dir", os.path.dirname(name))

            self.lineEdit_6.setText(name)

    def clear_all(self):
        "清除所有控件的数据"
        self.lineEdit_4.setText("")
        self.textBrowser_5.setText("")
        self.textBrowser_7.setText("")
        self.lineEdit_3.setText("")

        self.lineEdit_5.setText("")
        self.textBrowser_8.setText("")
        self.textBrowser_9.setText("")
        self.lineEdit_9.setText("")

        self.lineEdit_10.setText("")
        self.textBrowser_10.setText("")
        self.textBrowser_11.setText("")
        self.lineEdit_11.setText("")

        self.lineEdit_12.setText("")
        self.textBrowser_12.setText("")
        self.textBrowser_13.setText("")
        self.lineEdit_13.setText("")

        lineedits1 = [self.RSTN_DX, self.RSTN_DY, self.RSTN_DZ,
                      self.RSUP_DX, self.RSUP_DY, self.RSUP_DZ,
                      self.HANG_DX, self.HANG_DY, self.HANG_DZ,
                      self.SNUB_DX, self.SNUB_DY, self.SNUB_DZ]

        lineedits2 = [self.RSTN_SP, self.RSUP_SP, self.HANG_SP, self.SNUB_SP]

        lineedits3 = [self.RSTN_DX_2, self.RSTN_DY_2, self.RSTN_DZ_2,
                      self.RSUP_DX_2, self.RSUP_DY_2, self.RSUP_DZ_2,
                      self.HANG_DX_2, self.HANG_DY_2, self.HANG_DZ_2,
                      self.SNUB_DX_2, self.SNUB_DY_2, self.SNUB_DZ_2]
        lineedits4 = [self.RSTN_SP_2, self.RSUP_SP_2, self.HANG_SP_2, self.SNUB_SP_2]

        lineedits5 = [self.RSTN_DX_3, self.RSTN_DY_3, self.RSTN_DZ_3,
                      self.RSUP_DX_3, self.RSUP_DY_3, self.RSUP_DZ_3,
                      self.HANG_DX_3, self.HANG_DY_3, self.HANG_DZ_3,
                      self.SNUB_DX_3, self.SNUB_DY_3, self.SNUB_DZ_3]
        lineedits6 = [self.RSTN_SP_3, self.RSUP_SP_3, self.HANG_SP_3, self.SNUB_SP_3]

        lineedits7 = [self.RSTN_DX_4, self.RSTN_DY_4, self.RSTN_DZ_4,
                      self.RSUP_DX_4, self.RSUP_DY_4, self.RSUP_DZ_4,
                      self.HANG_DX_4, self.HANG_DY_4, self.HANG_DZ_4,
                      self.SNUB_DX_4, self.SNUB_DY_4, self.SNUB_DZ_4]
        lineedits8 = [self.RSTN_SP_4, self.RSUP_SP_4, self.HANG_SP_4, self.SNUB_SP_4]

        lvs = [self.RSTN_LV, self.SNUB_LV, self.RSUP_LV, self.HANG_LV,
               self.RSTN_LV_2, self.SNUB_LV_2, self.RSUP_LV_2, self.HANG_LV_2,
               self.RSTN_LV_3, self.SNUB_LV_3, self.RSUP_LV_3, self.HANG_LV_3,
               self.RSTN_LV_4, self.SNUB_LV_4, self.RSUP_LV_4, self.HANG_LV_4
               ]

        for group in [lineedits1, lineedits2, lineedits3, lineedits4, lineedits5, lineedits6, lineedits7, lineedits8,
                      lvs]:
            for line_e in group:
                line_e.setText("")

        self.RSTN.setChecked(False)
        self.SNUB.setChecked(False)
        self.RSUP.setChecked(False)
        self.HANG.setChecked(False)

        self.RSTN_2.setChecked(False)
        self.SNUB_2.setChecked(False)
        self.RSUP_2.setChecked(False)
        self.HANG_2.setChecked(False)

        self.RSTN_3.setChecked(False)
        self.SNUB_3.setChecked(False)
        self.RSUP_3.setChecked(False)
        self.HANG_3.setChecked(False)

        self.RSTN_4.setChecked(False)
        self.SNUB_4.setChecked(False)
        self.RSUP_4.setChecked(False)
        self.HANG_4.setChecked(False)

    def button_save_conf(self):
        """
        配置文件函数
        :return:
        """
        try:
            if os.path.exists(self.lineEdit_6.text()):
                self.clear_all()

                self.data_path = self.lineEdit_6.text()
                cal_flag = self.get_file_path()
                self.dir_num = 1
                if cal_flag:
                    self.max_path, self.prr_path, self.ppo_path, self.prd_path = cal_flag[0], cal_flag[1], cal_flag[2], \
                                                                                 cal_flag[4]
                    self.prc_path = cal_flag[3]
                    self.button_tmp_click()
                    self.treeWidget_2.clear()
                    self.treeWidget_2.setColumnCount(1)
                    self.treeWidget_2.expandAll()
                    file_list = []
                    extensions = ['.fre', '.ppo', '.prc', '.prd', '.max', '.pre', '.pri', '.prl', '.prr', '.tmp',
                                  '.txt']
                    file_dir = os.path.dirname(self.data_path)
                    name = os.path.basename(self.data_path)
                    fre_name = os.path.splitext(name)[0]
                    try:
                        root, dirs, files = list(os.walk(file_dir))[0]
                        for file in files:
                            file_name, suf = os.path.splitext(file)
                            file_name_shock = file_name + '_shock'
                            if (fre_name == file_name and suf in extensions) or (
                                    file_name_shock == file_name and suf in extensions):
                                file_list.append(file)

                        for opt_dir in dirs:
                            opt_name = os.path.basename(opt_dir)
                            opt_path = os.path.join(root, opt_dir)
                            if opt_name.startswith('optimization'):
                                shutil.rmtree(opt_path)
                    except Exception as e:
                        msg = str(e)
                        QMessageBox.information(self, '提示', '文件夹文件被使用中，请关闭：%s' % msg)

                    root = QTreeWidgetItem(self.treeWidget_2)
                    fileInfo = QFileInfo(os.path.dirname(self.data_path))
                    fileIcon = QFileIconProvider()
                    icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                    self.treeWidget_2.addTopLevelItem(root)
                    self.treeWidget_2.header().setMinimumSectionSize(800)
                    self.treeWidget_2.expandAll()
                    root.setText(0, os.path.dirname(self.data_path))
                    root.setIcon(0, QtGui.QIcon(icon))

                    for item in file_list:
                        try:
                            child = QTreeWidgetItem()
                            child.setText(0, item)
                            path_new = os.path.join(os.path.dirname(self.data_path), item)
                            fileInfo = QFileInfo(path_new)
                            fileIcon = QFileIconProvider()
                            icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                            child.setIcon(0, QtGui.QIcon(icon))
                            root.addChild(child)
                        except Exception as e:
                            print(e)
                if self.radioButton.isChecked():
                    self.chose_radio = self.radioButton.text()
                elif self.radioButton_2.isChecked():
                    self.chose_radio = self.radioButton_2.text()
                elif self.radioButton_3.isChecked():
                    self.chose_radio = self.radioButton_3.text()
                elif self.radioButton_4.isChecked():
                    self.chose_radio = self.radioButton_4.text()

                QMessageBox.information(self, '提示', '配置成功')
            else:
                QMessageBox.information(self, '提示', '请确认路径是否有效！')
        except Exception as e:
            print(e, '配置文件错误')

    @staticmethod
    def turn_date(self, timestamp):
        """转换时间"""
        date = datetime.datetime.fromtimestamp(timestamp)
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")
        return str_date

    def deal_file(self, item):
        try:
            name = item.text(0)
            file_path = os.path.join(os.path.dirname(self.data_path), name)
            size = os.path.getsize(file_path)
            mtime = os.path.getmtime(file_path)
            mtime = self.turn_date(self, timestamp=mtime)
            ctime = os.path.getctime(file_path)
            ctime = self.turn_date(self, timestamp=ctime)
            type1 = os.path.splitext(file_path)[-1]
            self.lineEdit1.setText('Name')
            self.lineEdit3.setText('Path')
            self.lineEdit5.setText('Type')
            self.lineEdit7.setText('Size')
            self.lineEdit9.setText('Creation Time')
            self.lineEdit11.setText('Update Time')
            self.lineEdit2.setText(name)
            self.lineEdit4.setText(file_path)
            self.lineEdit6.setText(type1)
            self.lineEdit8.setText(str(size))
            self.lineEdit10.setText(ctime)
            self.lineEdit12.setText(mtime)
        except Exception as e:
            print(e)

    def skim_file(self, item):
        try:
            name = item.text(0)
            file_path = os.path.join(os.path.dirname(self.data_path), name)
            with open(file_path, 'r', errors='ignore') as f:
                content = f.read()
                self.textBrowser_2.clear()
                self.stackedWidget.setCurrentIndex(4)
                self.textBrowser_2.setText(content)
        except Exception as e:
            print(e)

    def button_modul_click(self):
        if self.data_path:
            fre_dir = os.path.dirname(self.data_path)
            name, _ = QFileDialog.getOpenFileName(self, '选择模板文件', fre_dir, '报告模板(*.docx)')  # 起始路径
        else:
            name, _ = QFileDialog.getOpenFileName(self, '选择模板文件', r'C:/', '报告模板(*.docx)')
        self.lineEdit_7.setText(name)

    def button_output_click(self):
        if self.data_path:
            fre_dir = os.path.dirname(self.data_path)
            name, _ = QFileDialog.getSaveFileName(self, '另存为', fre_dir, '报告模板(*.docx)')
        else:
            name, _ = QFileDialog.getSaveFileName(self, '另存为', r'./', '报告模板(*.docx)')

        self.lineEdit_8.setText(name)

    def button_get_shock2(self):
        """
        导入其他.prd文件生成冲击谱
        :return:
        """
        if self.data_path:
            fre_dir = os.path.dirname(self.data_path)
            name, _ = QFileDialog.getOpenFileName(self, '选择.prd文件', fre_dir, '(*.prd *)')  # 起始路径
        else:
            name, _ = QFileDialog.getOpenFileName(self, '选择.prd文件', r'C:/', '(*.prd)')

        if name:
            self.textBrowser_3.clear()
            dir_name = os.path.dirname(name)
            filepath, tmpfilename = os.path.split(name)
            shotname, extension = os.path.splitext(tmpfilename)

            total_mass, frequency = ShockSpectrum().cal_shock(name)
            if len(total_mass.keys()) == len(frequency.keys()):
                # 冲击谱路径，以及各项内容
                shock_path, self.m_f_lines = ShockSpectrum().cal_a_v(total_mass, frequency, dir_name, shotname)
                shock_path = shock_path.replace('\\', '/')
                QMessageBox.information(self, '提示', '生成冲击谱成功，文件位置\n%s' % shock_path)
            else:
                QMessageBox.information(self, '提示', 'prd数据读取不匹配！请检查下源文件')

    def button_get_shock(self):
        """
        获取冲击谱文件
        :return:
        """
        try:
            if self.prd_path:
                self.textBrowser_3.clear()
                dir_name = os.path.dirname(self.prd_path)

                filepath, tmpfilename = os.path.split(self.prd_path)
                shotname, extension = os.path.splitext(tmpfilename)
                total_mass, frequency = ShockSpectrum().cal_shock(self.prd_path)
                if len(total_mass.keys()) == len(frequency.keys()):
                    # 冲击谱路径，以及各项内容
                    shock_path, self.m_f_lines = ShockSpectrum().cal_a_v(total_mass, frequency, dir_name, shotname)
                    shock_path = shock_path.replace('\\', '/')
                    QMessageBox.information(self, '提示', '生成冲击谱成功，文件位置\n%s' % shock_path)
                else:
                    QMessageBox.information(self, '提示', 'prd数据读取不匹配！请检查下源文件')
            else:
                QMessageBox.information(self, '提示', '请先配置prd文件！')
        except Exception as e:
            msg = str(e)
            QMessageBox.information(self, '提示', '异常:' + msg)

    def button_run_click(self):
        """
        开始生成报告
        :return:
        """

        if os.path.exists(self.data_path) and os.path.exists(self.lineEdit_7.text()) and self.lineEdit_8.text() \
                != '':

            if os.path.exists(self.lineEdit_8.text()):
                cover_ins = QMessageBox.question(self, '提示', "已存在该文件，是否覆盖?",
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if cover_ins == QMessageBox.Yes:
                    self.gen_report()
            else:
                self.gen_report()

        else:
            # print(self.data_path, self.lineEdit_7.text(), self.lineEdit_8.text())
            QMessageBox.information(self, '提示', '请确认路径是否有效,fre数据有没有配置！')

    def gen_report(self):
        """
        生成报告
        :return:
        """
        try:

            obj_rp = ExportReport(self.lineEdit_7.text(), self.data_path, self.lineEdit_8.text(), self.max_path,
                                  self.prr_path, self.ppo_path, self.prc_path)
            if obj_rp.read_template():
                save1 = QMessageBox.question(self, '提示', "导出成功，是否打开?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if save1 == QMessageBox.Yes:
                    obj_rp.open_docx(self.lineEdit_8.text())
            else:
                QMessageBox.information(self, '提示', '导出失败')
        except Exception as e:
            msg = str(e)
            if msg == "(-2147221005, '无效的类字符串', None, None)" or \
                    msg == "(-2147418111, '被呼叫方拒绝接收呼叫。', None, None)":
                QMessageBox.information(self, '提示', 'word版本不支持，请前往文档位置打开')
            else:
                QMessageBox.information(self, '提示', '异常:' + msg)

    def button_tmp_click(self):
        # 配置文件完成后，结果浏览
        try:

            tmp_path = GenTmp(self.data_path, self.max_path, self.prr_path, self.ppo_path, self.prc_path).gen_tmp()
            self.tmp_path = tmp_path
            print(self.tmp_path)
            self.init_list_widget(tmp_path)
        except Exception as e:
            print(e)
            QMessageBox.information(self, '提示', '结果未正确提取，请检查.fre .max .prr .ppo .prc!')

    def init_list_widget(self, path):
        """
        初始化listwidget
        :param path: 结算结果路径
        :return:
        """
        support_nodes = []

        if os.path.exists(path):
            group_list1 = [self.listWidget_3, self.listWidget_4, self.listWidget_5]
            for i in group_list1:
                i.clear()
            with open(path, 'r') as f:
                while True:
                    line = f.readline()
                    if "@支撑+" in line:
                        # self.listWidget_3.addItem(line.split('+')[1].strip())
                        support_nodes.append(line.split('+')[1].strip())

                    elif "@设备接管" in line:
                        self.listWidget_4.addItem(line.split('+')[1].strip())
                    elif "@位移输出" in line:
                        self.listWidget_5.addItem(line.split('@')[1].strip())

                    if not line:
                        break
            support_nodes.sort(key=lambda x: x.split('节点')[1])
            self.listWidget_3.addItems(support_nodes)
        else:
            QMessageBox.information(self, "提示", "请确认数据已生成或者在导出报告页面选择数据目录！")

    def list_item_index_changed(self, item):
        """
        点击结果浏览界面item，获取对应的结果内容
        :param item: 所点击的item
        :return:
        """

        str_data = StringIO()
        str_data.truncate(0)
        str_data.seek(0)
        self.textBrowser.clear()

        if os.path.exists(self.tmp_path):

            with open(self.tmp_path, 'r') as f:
                while True:
                    line = f.readline()

                    if item.text() in line:
                        if '+' in line:
                            if line.split('+')[1] != item.text():
                                print(line)

                        while line:
                            line = f.readline()
                            if line.strip() != '':
                                if line[0] == '@':
                                    break
                            str_data.write(line + '\n')
                            self.textBrowser.setText(str_data.getvalue())

                    if not line:
                        break

        else:
            QMessageBox.information(self, '提示', '结果未正确提取，请检查.fre .max .prr .ppo .prc!')

    def page_show(self):
        """
        fre配置界面
        :return:
        """
        self.stackedWidget.setCurrentIndex(0)

    def page1_show(self):
        """
        结果快速查询
        :return:
        """
        self.stackedWidget.setCurrentIndex(2)

    def page2_show(self):
        """
        材料库界面
        :return:
        """
        self.stackedWidget.setCurrentIndex(1)
        current = self.stackedWidget.currentIndex()
        if current != 1:
            QMessageBox.information(self, '提示', '导出失败')

    def page3_show(self):
        """
        报告界面
        :return:
        """
        self.stackedWidget.setCurrentIndex(3)

    def page4_show(self):
        """
        支吊架界面
        :return:
        """
        self.stackedWidget.setCurrentIndex(5)

    def page5_show(self):
        """
        支吊架界面
        :return:
        """
        self.stackedWidget.setCurrentIndex(6)

    def closeEvent(self, event):
        """我们创建了一个消息框，上面有俩按钮：Yes和No.第一个字符串显示在消息框的标题栏，第二个字符串显示在对话框，
              第三个参数是消息框的俩按钮，最后一个参数是默认按钮，这个按钮是默认选中的。返回值在变量reply里。"""
        save1 = QMessageBox.question(self, '提示', "是否保存数据?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if save1 == QMessageBox.Yes:
            self.button_save_click()

        reply = QMessageBox.question(self, '提示', "确定退出程序",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def button_material_click(self):
        """打开材料库操作"""

        materials_dir = get_default_path("materials_dir")
        name, _ = QFileDialog.getOpenFileName(self, '打开材料库文件', materials_dir,
                                              '数据文件(*.xml)')
        self.library_path = name

        is_read = False
        if os.path.isfile(self.library_path):
            set_default_path("materials_dir", os.path.dirname(self.library_path))
            try:
                # 开始解析xml文件
                new_xml, bool_value = make_xml(self.library_path)
                if new_xml and bool_value:
                    is_read = True
                else:
                    QMessageBox.information(self, '提示', '未读到文件内容,' + new_xml)
                if is_read:
                    self.treeWidget.clear()

                    dom = et.parse(new_xml)
                    self.dom = dom
                    root = dom.getroot()  # 获取根节点
                    print(root.text)
                    materials = root.findall('.//DirectXML//MATERIAL')
                    print(materials)
                    if len(materials):
                        for material in materials:
                            material_name = material.get('name')
                            tree_item = QTreeWidgetItem(self.treeWidget)
                            tree_item.setIcon(0, QIcon(':/picture/images/material.ico'))
                            tree_item.setText(0, material_name)

                            self.treeWidget.addTopLevelItem(tree_item)
                            self.treeWidget.header().setMinimumSectionSize(1000)
                            items = material.findall('Item')  # 查找具体材料

                            for item in items:
                                item_name = item.get('name')
                                child = QTreeWidgetItem()
                                child.setText(0, item_name)  # 绘制材料树形图
                                child.setIcon(0, QIcon(':/picture/images/toolbar.ico'))
                                tree_item.addChild(child)

            except Exception as e:
                msg = str(e)
                QMessageBox.information(self, '提示', '材料库格式有问题，请检查')

    def button_save_click(self):
        """
        保存材料库
        :return:
        """
        try:
            if os.path.exists(self.library_path):
                if QMessageBox.question(self, '提示', '确定保存修改吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes) \
                        == QMessageBox.Yes:
                    root = self.dom.getroot()
                    indent(root)
                    self.dom.write(self.library_path, encoding='UTF-8')
            # else:
            #     QMessageBox.information(self, '提示', '未打开材料库')

        except Exception as e:
            print(e)

    def item_click(self, item, column):
        """
        tree树结构点击功能
        :param item: 被单击的项目对象
        :param column:  就是被单击的序列号
        :return:
        """
        # item = self.treeWidget.currentItem()

        if item.parent():
            # 判断当前点击位置是否是材料上还是材料库
            root = self.dom.getroot()
            materials = root.findall('.//MATERIAL')
            if len(materials):
                for material in materials:
                    name = material.get('name')
                    print(name)
                    # 拿到材料库名字
                    if name == item.parent().text(column):
                        items = material.findall('Item')
                        # 寻找该软件下所有的Item单个材料
                        for j in items:
                            all_cards = j.findall('Card')
                            matd_card = []
                            print(j.text)
                            print('hello')
                            if j.get('name') == item.text(column):

                                for card in all_cards:
                                    if card.get('name') == 'Desc':
                                        self.textEdit.setText(card.text)

                                    # 处理math数据
                                    if card.get('name') == 'MATH':
                                        str_math = card.text.split()
                                        self.cd.setText(str_math[1][3:])
                                        self.ex.setText(str_math[2][3:])
                                        self.ty.setText(str_math[3][3:])
                                        self.tx.setText(str_math[4][3:])
                                    if card.get('name') == 'MATD':
                                        matd_card.append(card)
                                if len(matd_card):
                                    self.tableWidget.blockSignals(True)
                                    index = 0
                                    self.tableWidget.setRowCount(0)
                                    self.tableWidget.clearContents()
                                    self.tableWidget.setRowCount(len(matd_card))
                                    # 判断属性个数和长度
                                    for matd_node in matd_card:
                                        str_matd = matd_node.text.split()
                                        list1 = str_matd[1:]
                                        list2 = [x[:2] for x in list1]

                                        if 'SM=' in matd_node.text:
                                            self.tableWidget.setHorizontalHeaderLabels(list2)
                                            self.tableWidget.setColumnCount(len(list2))
                                            for num in range(len(list1)):
                                                self.tableWidget.setItem(index, num,
                                                                         QTableWidgetItem(list1[num][3:]))

                                        else:
                                            if 6 == self.tableWidget.columnCount():
                                                self.tableWidget.removeColumn(4)
                                            for num in range(len(list1)):
                                                self.tableWidget.setItem(index, num,
                                                                         QTableWidgetItem(list1[num][3:]))
                                        index += 1
                                    self.tableWidget.blockSignals(False)

            if not self.first_init_math:
                self.first_init_math = True
            self.textEdit.textChanged.connect(self.text_edit)  # 材料描述编辑
            self.cd.textChanged.connect(self.math_changed)  # 材料属性发生变化的时候监控数据
            self.ex.textChanged.connect(self.math_changed)
            self.ty.textChanged.connect(self.math_changed)
            self.tx.textChanged.connect(self.math_changed)
            if not self.first_init_matd:
                self.first_init_matd = True
            self.tableWidget.cellChanged.connect(self.table_cell_changed)  # 材料表格变动

    def add_row(self):
        """增加一行"""
        cur_total_row = self.tableWidget.rowCount()
        curr_item = self.treeWidget.currentItem()
        if not cur_total_row:
            return
        if curr_item:

            root = self.dom.getroot()
            items = root.findall('.//MATERIAL/Item')
            self.tableWidget.insertRow(cur_total_row)
            curr_row = cur_total_row

            for item in items:
                if item.get('name') == curr_item.text(0) and 6 == self.tableWidget.columnCount():

                    matd_node = et.Element('Card')
                    matd_node.set('name', 'MATD')
                    matd_node.text = "MATD TE=0 EH=0 EX=0 SH=0 SM=0 SY=0"
                    item.append(matd_node)
                    for i in range(6):
                        self.tableWidget.blockSignals(True)
                        self.tableWidget.setItem(curr_row, i, QTableWidgetItem('0'))
                        self.tableWidget.blockSignals(False)

                elif item.get('name') == curr_item.text(0) and 5 == self.tableWidget.columnCount():
                    matd_node = et.Element('Card')
                    matd_node.set('name', 'MATD')
                    matd_node.text = "MATD TE=0  EH=0 EX=0 SH=0 SY=0"
                    item.append(matd_node)

    def del_row(self):
        # 删除一行
        try:
            cur_total_row = self.tableWidget.rowCount()
            if not cur_total_row:
                return
            reply = QMessageBox.question(self, '确认', '确定删除数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                curr_item = self.treeWidget.currentItem()
                root = self.dom.getroot()
                items = root.findall('.//MATERIAL/Item')
                for item in items:
                    if item.get('name') == curr_item.text(0):
                        r = self.tableWidget.currentIndex().row()
                        all_cards = item.findall('Card')
                        matd_nodes = [card for card in all_cards if card.get('name') == 'MATD']
                        item.remove(matd_nodes[r])
                        self.tableWidget.removeRow(r)
        except Exception as e:
            print(e)

    def add_material_lib(self):
        """新增材料库"""

        root = self.dom.getroot()
        new_xml_node = root.find('.//DirectXML')
        while True:
            text, ok = QInputDialog.getText(self, '增加材料库', '请输入材料库名称')
            if not ok:
                break
            if not text or text in [mat.get('name') for mat in root.findall('.//MATERIAL')]:
                QMessageBox.information(self, '提示', '该材料库已存在，请重新输入')
            else:
                new_mat = et.Element('MATERIAL')
                new_mat.set('name', text)
                id_label = et.SubElement(new_mat, 'ID')
                # 创建ID标签
                id_label.text = text

                new_xml_node.append(new_mat)

                tree_item = QTreeWidgetItem(self.treeWidget)
                self.treeWidget.addTopLevelItem(tree_item)
                tree_item.setText(0, text)
                tree_item.setIcon(0, QIcon(":/picture/images/material.ico"))
                break

    def del_material_lib(self):
        """删除材料库"""
        curr_item = self.treeWidget.currentItem()
        reply = QMessageBox.question(self, '确认', '确定删除数据？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            root = self.dom.getroot()
            mat_nodes = root.findall('.//MATERIAL')
            directxml_node = root.find('DirectXML')
            for mat_node in mat_nodes:
                if curr_item.text(0) == mat_node.get('name'):
                    directxml_node.remove(mat_node)
                    root_index = self.treeWidget.indexOfTopLevelItem(curr_item)
                    self.treeWidget.takeTopLevelItem(root_index)

    def add_material_click(self):
        """增加材料操作"""
        curr_item = self.treeWidget.currentItem()
        root = self.dom.getroot()
        parent_mat = ''
        if curr_item.parent():
            for mat in root.findall('.//MATERIAL'):
                if mat.get('name') == curr_item.parent().text(0):
                    parent_mat = mat
        else:
            for mat in root.findall('.//MATERIAL'):
                if mat.get('name') == curr_item.text(0):
                    parent_mat = mat

        while True:
            text, ok = QInputDialog.getText(self, '增加材料', '请输入材料名称')
            if not ok:
                break

            if not text or text in [item.get('name') for item in parent_mat.findall('.//Item')]:
                QMessageBox.information(self, '提示', '请输入有效名称')
            else:
                new_item = QTreeWidgetItem()
                new_item.setText(0, text)
                new_item.setIcon(0, QIcon(':/picture/images/toolbar.ico'))
                new_ele = et.Element('Item')
                new_ele.set('name', text)
                id_node = et.Element('ID')
                id_node.text = text
                desc_node = et.Element('Card')
                desc_node.set('name', 'Desc')
                desc_node.text = "* MATERIAL: "
                math_node = et.Element('Card')
                math_node.set('name', 'MATH')
                math_node.text = "MATH CD=0 EX=0 TY=0 TX=0"
                matd_node = et.Element('Card')
                matd_node.set('name', 'MATD')
                matd_node.text = "MATD TE=0 EH=0 EX=0 SH=0 SM=0 SY=0"
                material = root.findall('.//MATERIAL')
                if curr_item.parent():
                    for m in material:
                        if m.get('name') == curr_item.parent().text(0):
                            m.append(new_ele)
                            new_ele.extend([id_node, desc_node, math_node, matd_node])
                    curr_item.parent().addChild(new_item)

                else:
                    for m in material:
                        if m.get('name') == curr_item.text(0):
                            m.append(new_ele)
                            new_ele.extend([id_node, desc_node, math_node, matd_node])
                    curr_item.addChild(new_item)

                break

    def del_material_click(self, column):
        """删除材料操作"""
        curr_item = self.treeWidget.currentItem()
        tip = '确定删除材料' + curr_item.text(column)

        reply = QMessageBox.question(self, '确认', tip, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            root = self.treeWidget.invisibleRootItem()
            root1 = self.dom.getroot()
            el_p = root1.findall('.//MATERIAL/Item')

            m = root1.findall('.//MATERIAL')
            for m1 in m:
                if m1.get('name') == curr_item.parent().text(column):
                    for i in el_p:
                        if i.get('name') == curr_item.text(column):
                            m1.remove(i)

            for item in self.treeWidget.selectedItems():
                (item.parent() or root).removeChild(item)

    def text_edit(self):
        # text区域的数据变化
        curr_item = self.treeWidget.currentItem()
        root = self.dom.getroot()
        nodes = root.findall('.//MATERIAL/Item')
        for node in nodes:
            if curr_item.text(0) == node.get('name'):
                cards = node.findall('Card')
                for card in cards:
                    if card.get('name') == 'Desc':
                        card.text = self.textEdit.toPlainText()

    def math_changed(self):
        """"math 数据发生变化的时候"""
        curr_item = self.treeWidget.currentItem()
        root = self.dom.getroot()
        nodes = root.findall('.//MATERIAL/Item')
        for node in nodes:
            if curr_item.text(0) == node.get('name'):
                cards = node.findall('Card')
                for card in cards:
                    if card.get('name') == 'MATH':
                        card.text = "MATH CD=" + self.cd.text() + " EX=" + self.ex.text() \
                                    + " TY=" + self.ty.text() + " TX=" + self.tx.text()

    def table_cell_changed(self, row, col):
        """matd数据发生变化的时候"""

        curr_item = self.treeWidget.currentItem()
        root = self.dom.getroot()
        m_nodes = root.findall('.//MATERIAL')
        for m_node in m_nodes:
            # 遍历材料库
            if m_node.get('name') == curr_item.parent().text(0):
                nodes = m_node.findall('Item')
                curr_row = row
                curr_cell = self.tableWidget.item(row, col)
                content = curr_cell.text()
                if not is_number(content):
                    QMessageBox.about(self, '提示', '请输入数字')
                    curr_cell.setText('0')

                for node in nodes:
                    # 遍历单个材料出来
                    if curr_item.text(0) == node.get('name'):
                        all_cards = node.findall('Card')
                        # matd_nodes = []
                        matd_nodes = [card for card in all_cards if card.get('name') == 'MATD']
                        # for card in all_cards:
                        #     if card.get('name') == 'MATD':
                        #         matd_nodes.append(card)
                        if self.tableWidget.columnCount() == 6:
                            matd_nodes[curr_row].text = "MATD TE=" + self.tableWidget.item(curr_row, 0).text() \
                                                        + " EH=" + self.tableWidget.item(curr_row, 1).text() \
                                                        + " EX=" + self.tableWidget.item(curr_row, 2).text() \
                                                        + " SH=" + self.tableWidget.item(curr_row, 3).text() \
                                                        + " SM=" + self.tableWidget.item(curr_row, 4).text() \
                                                        + " SY=" + self.tableWidget.item(curr_row, 5).text()

                        if self.tableWidget.columnCount() == 5:
                            matd_nodes[curr_row].text = "MATD TE=" + self.tableWidget.item(curr_row, 0).text() \
                                                        + " EH=" + self.tableWidget.item(curr_row, 1).text() \
                                                        + " EX=" + self.tableWidget.item(curr_row, 2).text() \
                                                        + " SH=" + self.tableWidget.item(curr_row, 3).text() \
                                                        + " SY=" + self.tableWidget.item(curr_row, 4).text()

    def right_click_menu(self, pos):
        """
        点击tree，获取右键菜单
        :param pos: 点击位置
        :return: 无返回值
        """
        item = self.treeWidget.currentItem()
        # item1
        if not self.treeWidget.itemAt(pos):
            return

        if item.parent():
            try:
                self.treeWidget.contextMenu = QMenu()  # 创建对象
                self.treeWidget.actionA = self.treeWidget.contextMenu.addAction(u'增加材料')  # 添加动作
                self.treeWidget.actionB = self.treeWidget.contextMenu.addAction(u'删除材料')
                self.treeWidget.actionA.triggered.connect(self.add_material_click)
                self.treeWidget.actionB.triggered.connect(self.del_material_click)

                self.treeWidget.contextMenu.move(self.treeWidget.mapToGlobal(pos))
                self.treeWidget.contextMenu.show()  # 显示

            except Exception as e:
                print(e)
        elif item:
            try:
                self.treeWidget.contextMenu = QMenu()  # 创建对象
                self.treeWidget.actionA = self.treeWidget.contextMenu.addAction(u'新增材料库')  # 添加动作
                self.treeWidget.actionB = self.treeWidget.contextMenu.addAction(u'删除材料库')
                self.treeWidget.actionC = self.treeWidget.contextMenu.addAction(u'新增材料')
                self.treeWidget.actionA.triggered.connect(self.add_material_lib)
                self.treeWidget.actionB.triggered.connect(self.del_material_lib)
                self.treeWidget.actionC.triggered.connect(self.add_material_click)
                self.treeWidget.contextMenu.move(self.treeWidget.mapToGlobal(pos))
                self.treeWidget.contextMenu.show()  # 显示

            except Exception as e:
                print(e)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoMain()
    bindwidget = ActivationWidget()
    if bindwidget.verify("licence.txt"):
        demo.show()
    else:
        choice = QMessageBox.critical(
            None,
            '提示',
            '尚未配置许可文件或许可文件无效，请重新配置许可文件')
        bindwidget.show()

    # 包含框架得最大化显示
    # demo.showMaximized()
    # demo.showFullScreen()  不包含框架
    #488157184730
    sys.exit(app.exec_())
