from ast import Try
from re import S
import sys
import os
import datetime
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QGroupBox,QGridLayout,QLineEdit,QLabel,QTextBrowser
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5.QtCore import Qt, QFileInfo, QRegExp
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTreeWidgetItem, \
    QFileIconProvider, QMenu, QHeaderView, QTableWidgetItem, QInputDialog, QListWidgetItem



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

        self.setWindowTitle("获取许可文件")
        self.resize(600, 400)
        self.setCentralWidget(QWidget())
        self.main_layout = QVBoxLayout(self.centralWidget())

        self.holder = QGroupBox()
        vbox = QGridLayout()
        self.macadress = QLineEdit("")
        self.macadress.setObjectName('macadress')
        lb1 = QLabel('物理地址:')
        vbox.addWidget(lb1,0,3,1,1)
        vbox.addWidget(self.macadress,0,5,1,1)

        self.cutofftime = QLineEdit()
        self.cutofftime.setObjectName('cutofftime')
        lb2 = QLabel('截止日期:')
        vbox.addWidget(lb2,1,3,1,1)
        vbox.addWidget(self.cutofftime,1,5,1,1)

        self.activationpath = QLineEdit()
        self.activationpath.setObjectName('activationpath')
        lb2 = QLabel('保存路径:')
        vbox.addWidget(lb2,2,3,1,1)
        vbox.addWidget(self.activationpath,2,5,1,1)
        self.savepathbutton = QPushButton()
        self.savepathbutton.setText("选择路径")
        vbox.addWidget(self.savepathbutton,2,10,1,3)
        self.savepathbutton.clicked.connect(self.choosepath)
        
        self.holder.setLayout(vbox)
        self.main_layout.addWidget(self.holder)
        #self.savepathbutton.clicked.connect(self.choosepath)
        # self.holder.hide()

        self.loginbutton = QPushButton()
        self.loginbutton.setText("生成许可文件")
        self.main_layout.addWidget(self.loginbutton)
        self.loginbutton.clicked.connect(self.get_verify_doc)

    def choosepath(self):
        savepath = QFileDialog.getExistingDirectory(self, "选择路径")
        self.activationpath.setText(savepath)
              

    def get_verify_doc(self):
        Etherstr = ''
        etable = {'A':'10','B':'11','C':'12','D':'13','E':'14','F':'15'}
        for c in self.get_value('macadress')+self.dateformate(self.get_value('cutofftime')):
            if c.isalpha() or c.isdigit(): 
                if c.isalpha():
                    if c.upper() in etable:
                        Etherstr += str(int(etable[c.upper()])%10)
                    else:
                        QMessageBox.critical(
                            None,
                            '错误',
                            '存在非法字符,物理地址真能为数字和字母a~f')
                        return            
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
        
        
        if self.get_value("activationpath") == "":
            QMessageBox.critical(
                None,
                '错误',
                '请选择保存路径')
        elif len(self.dateformate(self.get_value('cutofftime'))) != 8:
            QMessageBox.critical(
                None,
                '错误',
                '日期必须用8位数字表示')
        else:
            file = self.get_value("activationpath")+"/license.txt"
            file = os.path.realpath(file)
            if os.path.exists(file):
                choice = QMessageBox.question(
                None,
                '确认',
                '文件已存在,是否覆盖')
                if choice == QMessageBox.Yes:
                    self.savefile(file,licence)
            else:
                self.savefile(file,licence)        

    def savefile(self,file,licence):
        with open(file, "w",encoding='UTF-8') as f:
            f.write(licence+self.get_value('cutofftime'))
        choice = QMessageBox.question(
                    None,
                    '确认',
                    '保存成功，是否打开文件路径')
        if choice == QMessageBox.Yes:  
            os.system(f'explorer /select, {file}')
        else:
            pass

    def get_value(self, object_name):
        try:
            return self.findChild(QLineEdit, object_name).text()
        except Exception as e:
            print(object_name)
    
    def dateformate(self,date):
        newdate = ""
        for c in date:
            if c.isdigit():
                newdate += c

        return newdate

if __name__ == '__main__':
    app = QApplication(sys.argv)
    get_activation_widget = ActivationWidget()
    get_activation_widget.show()
    sys.exit(app.exec_())
                


    

    


    

    