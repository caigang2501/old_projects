import sys
from datetime import datetime
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QLabel, QRadioButton, \
    QGridLayout, QDateEdit, QComboBox, QApplication, QFileDialog
from functools import wraps
from traceback import print_exc
from random import choices
import string


def catch_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("**%s 出错**" % func.__name__)
            print(print_exc())

    return wrapper


class ToolUI(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCentralWidget(QWidget())
        self.setWindowTitle("license 生成工具")
        self.setGeometry(300, 300, 800, 400)
        self.centralWidget().setContentsMargins(30, 30, 30, 30)

        self.main_layout = QGridLayout(self.centralWidget())
        self.main_layout.setHorizontalSpacing(0)
        self.main_layout.setVerticalSpacing(10)

        self.centralWidget().setLayout(self.main_layout)
        self.initUI()  # 初始化控件设置及布局
        self.initQss()  # 初始化样式
        self.initEvent()  # 初始化事件
        self.init()

    def initUI(self):
        """初始化界面"""

        # 定义所有的控件
        label_user_id = QLabel("用户设备id   ")
        label_user_id.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_user_desc = QLabel("用户信息   ")
        label_user_desc.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_begin_time = QLabel("生效时间   ")
        label_begin_time.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_end_time = QLabel("过期时间   ")
        label_end_time.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        label_save_path = QLabel("保存路径   ")
        label_save_path.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.line_user_id = QLineEdit()  # 用户设备id输入框
        self.line_user_desc = QLineEdit()  # 用户描述
        self.radio_start = QRadioButton("当前立即生效")
        self.radio_start.setChecked(True)

        self.date_start = QDateEdit()
        cur_date = datetime.now().date()
        self.date_start.setDate(cur_date)
        self.use_period = QComboBox()  # 使用时长
        self.use_period.addItems(["1个月", "3个月", "6个月", "12个月", "24个月", "36个月"])
        self.date_end = QDateEdit()
        self.line_save_path = QLineEdit()
        self.button_license_path = QPushButton("选择")
        self.button_license_gen = QPushButton("生成license")

        # 对所有控件进行布局
        lay = self.main_layout
        lay.addWidget(label_user_id, 1, 1, 1, 1)  # 行 、 列 行范围 列范围     # 一共10列
        lay.addWidget(self.line_user_id, 1, 3, 1, 8)

        lay.addWidget(label_user_desc, 2, 1, 1, 1)
        lay.addWidget(self.line_user_desc, 2, 3, 1, 8)

        lay.addWidget(label_begin_time, 3, 1, 1, 1)
        lay.addWidget(self.radio_start, 3, 3, 1, 2)
        lay.addWidget(self.date_start, 3, 7, 1, 2)

        lay.addWidget(label_end_time, 4, 1, 1, 1)
        lay.addWidget(self.use_period, 4, 3, 1, 2)
        lay.addWidget(self.date_end, 4, 7, 1, 2)

        lay.addWidget(label_save_path, 5, 1, 1, 1)
        lay.addWidget(self.line_save_path, 5, 3, 1, 7)
        lay.addWidget(self.button_license_path, 5, 10, 1, 1)

        lay.addWidget(self.button_license_gen, 6, 5, 1, 2)

    def initQss(self):
        self.setStyleSheet(qss)

    def initEvent(self):
        self.button_license_path.clicked.connect(self.license_path_slot)
        self.button_license_gen.clicked.connect(self.gen_license_slot)

    def init(self):
        self.encryptor = Safety()

    def get_config(self):
        user_id = self.line_user_id.text()
        user_desc = self.line_user_desc.text()
        start_time = self.date_start.text()
        end_time = self.date_end.text()
        save_path = self.line_save_path.text()

        return {
            "user_id": user_id,
            "user_desc": user_desc,
            "start_time": start_time,
            "end_time": end_time,
            "save_path": save_path,
        }

    def gen_license_slot(self, *args):

        # 加密
        user_id = self.line_user_id.text()
        start_time = self.date_start.text()
        end_time = self.date_end.text()

        data = "@@@".join([user_id, start_time, end_time])

        data_sign = self.encryptor.get_aes_cbc(data)

        print(data_sign)

    @catch_error
    def license_path_slot(self, *args):
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹", r"C:/")  # 起始路径
        if not directory:
            return
        self.line_save_path.setText(directory)


qss = """
    QMainWindow {font-size: 15px;}
    QLabel {font-size:15px;}
    QComboBox {font-size:15px;}
"""

private_key = "gAAAAABaatPu9ATeOyfnPfsBzdOAHFW2ZVJGhhLYDO-1svENY7_PgBfewohSJrqXXvTGD_GXBuf-Eln5cIBRZZA7c_f95zSsDw=="

import base64
from Crypto.Cipher import AES


class Safety:
    the_salt = "random_salt"
    the_key = "random_key"

    # AES加密，CBC模式
    def get_aes_cbc(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(self.the_key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CBC, iv)  # 初始化加密器，key,iv使用同一个
        encrypt_bytes = aes.encrypt(self.pkcs7padding_tobytes(the_string))  # 进行aes加密
        encrypted_text = str(base64.b64encode(encrypt_bytes), encoding='utf-8')  # 用base64转成字符串形式
        return encrypted_text

    # AES解密，CBC模式
    def back_aes_cbc(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(self.the_key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CBC, iv)  # 初始化加密器，key,iv使用同一个
        decrypted_base64 = base64.b64decode(the_string)  # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64), encoding='utf-8')  # 执行解密密并转码返回str
        decrypted_text_last = self.pkcs7unpadding(decrypted_text)  # 去除填充处理
        return decrypted_text_last

    #######填充相关函数#######
    def pkcs7padding_tobytes(self, text):
        return bytes(self.pkcs7padding(text), encoding='utf-8')

    def pkcs7padding(self, text):
        bs = AES.block_size
        ####tips：utf-8编码时，英文占1个byte，而中文占3个byte####
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        ####################################################
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding  # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        return text + padding_text

    def pkcs7unpadding(self, text):
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]

def validate_device(device_code, sign):
    pass



# string = "aaaaaaaaaabbbbbbbbbbaaaaaadaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2011/02/12"
# ace = Safety()
# p = ace.get_aes_cbc(string)
# s = ace.back_aes_cbc(p)
# print("加密后：", p)
# print("解密后：", s)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ToolUI()
    window.show()
    # 包含框架得最大化显示
    # window.showMaximized()
    # window.showFullScreen()  不包含框架

    sys.exit(app.exec_())
