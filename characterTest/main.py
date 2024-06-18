# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
import time
import datetime
import _thread
import verifyTest
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from constent import *
from str2pdf import draw_text,draw_table,generatepdf,draw_little_title
from utils import *

class LoginWidget(QMainWindow):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)

        self.setWindowTitle("login")
        self.resize(600, 400)
        self.setCentralWidget(QWidget())
        self.main_layout = QVBoxLayout(self.centralWidget())

        self.VERIFYCODE = "123"

        holder = QGroupBox("手机验证登录")
        holder.setLayout(self.init_group_layout(loginfo))
        self.main_layout.addWidget(holder)


        self.loginbutton = QPushButton()
        self.loginbutton.setText("登录")
        self.main_layout.addWidget(self.loginbutton)
        self.loginbutton.clicked.connect(self.runlogin)

    def runlogin(self):
        if self.get_value('verifycode') == self.VERIFYCODE:
            main.setWindowTitle(self.get_value("name")+'    '+str(datetime.datetime.now())[:10])
            login.hide()
            main.show()
        else:
            QMessageBox.critical(
                None,
                '错误',
                '验证码错误')

    def getname(self):
        return self.get_value("name")

    def sendverify(self):
        self.VERIFYCODE = verifyTest.getVerifyCode(self.get_value("phonenumber"))
        self.verify.setDisabled(True)
        _thread.start_new_thread(self.counttime())

    def init_group_layout(self, item_list):
        vbox = QGridLayout()
        for index, item in enumerate(item_list):

            # 布局中定位行列
            offset = (index & 1) * 10  # index=1,3,5,7,9的会偏移10个单位
            row = index // 2  # 在坐标系中的行数

            # 初始化label并设置文字右对齐
            lb = QLabel(item["label"])
            lb.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

            # 初始化输入框，并设置默认值，setObjectName 设置变量命方便对该输入框取值
            le = QLineEdit()
            # le.setText(item.get("default", ""))
            le.setObjectName(item["var_name"])

            vbox.addWidget(lb, row, offset, 1, 3)
            vbox.addWidget(le, row, offset+3, 1, 1)

        self.verify = QPushButton()
        self.verify.setText("发送验证码")
        self.verify.clicked.connect(self.sendverify)
        vbox.addWidget(self.verify, 1, 11, 1, 2)
        return vbox


    def counttime(self):
        for i in range(60):
            self.verify.setText(str(60-i))
            time.sleep(1)
        self.verify.setText('重新发送')
        self.verify.setDisabled(False)

    def get_value(self, object_name):
        try:
            return self.findChild(QLineEdit, object_name).text()
        except Exception as e:
            print(object_name)

class MainWidget(QMainWindow):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        #self.scores 用于记录每题得分的数组
        #self.choocedAnswer 记录所选择的答案
        #self.QUESTIONNUMBER = 0 记录当前题号
        #self.setA 用于计分算法的选择依据
        #self.content 生成PDF文件的类容
        self.scores = [0]*188
        self.standardscore = []
        self.choocedAnswer = [0]*188
        self.QUESTIONNUMBER = 0
        self.setA = {28,53,54,77,78,102,103,127,128,152,153,177,178}
        self.content = []
        self.first = 1 #判断是否为第一次下载
        self.FIRSTDOWLOADPATH = ''

        #画出主界面
        self.setWindowTitle("psycologyTest")
        self.resize(600, 400)
        self.setCentralWidget(QWidget())
        self.main_layout = QVBoxLayout(self.centralWidget())

        self.mainString = ""
        self.textview = QTextBrowser()
        # self.textview.setFixedSize(200,200)
        self.textview.setText(questions[str(self.QUESTIONNUMBER)])
        self.main_layout.addWidget(self.textview)


        #添加按钮并设置响应函数
        # self.radioA 选项A按钮
        # self.radioB 选项B按钮
        # self.radioC 选项C按钮
        # self.formerbutton 上一题按钮
        # self.nextbutton   下一题按钮
        self.radioA = QRadioButton()
        self.radioA.toggled.connect(self.runradioA)
        self.main_layout.addWidget(self.radioA)
        self.radioB = QRadioButton()
        self.radioB.toggled.connect(self.runradioB)
        self.main_layout.addWidget(self.radioB)
        self.radioC = QRadioButton()
        self.radioC.toggled.connect(self.runradioC)
        self.main_layout.addWidget(self.radioC)

        self.formerbutton = QPushButton()
        self.formerbutton.setText("上一题")
        # self.formerbutton.setFixedSize(60,30)
        self.main_layout.addWidget(self.formerbutton)
        self.formerbutton.clicked.connect(self.runformer)

        self.nextbutton = QPushButton()
        self.nextbutton.setText("下一题")
        self.main_layout.addWidget(self.nextbutton)
        self.nextbutton.clicked.connect(self.runnext)

        #添加路径的QLineEdit，和选择路径按钮
        self.holder = QGroupBox()
        vbox = QGridLayout()
        self.pathline = QLineEdit("D:")
        self.savepathbutton = QPushButton()
        self.savepathbutton.setText("选择路径")
        vbox.addWidget(self.pathline,0,0,1,7)
        vbox.addWidget(self.savepathbutton,0,10,1,3)
        self.holder.setLayout(vbox)
        self.main_layout.addWidget(self.holder)
        self.savepathbutton.clicked.connect(self.choosepath)
        self.holder.hide()

        #t添加保存按钮
        self.downloadbutton = QPushButton()
        self.downloadbutton.setText("保存")
        self.main_layout.addWidget(self.downloadbutton)
        self.downloadbutton.clicked.connect(self.download)
        self.downloadbutton.hide()

    def choosepath(self):
        savepath = QFileDialog.getExistingDirectory(self, "选择路径")
        self.pathline.setText(savepath)


    def download(self):
        # path = self.pathline.text()+"/"+login.getname() +".txt"
        # with open(path, "wt") as out_file:
        #     out_file.write(self.mainString)
        if self.first:
            self.FIRSTDOWLOADPATH = self.pathline.text()
            generatepdf(self.content,login.getname(),self.pathline.text())
            self.first = 0
        else:
            if self.pathline.text() != self.FIRSTDOWLOADPATH:
                copyfile(self.FIRSTDOWLOADPATH+'/'+login.getname()+'.pdf', self.pathline.text())  # 复制文件



    #跳转到上一题的函数
    #设置上一题所选答案
    #设置上一题的题目和答案到UI
    def runformer(self):
        self.QUESTIONNUMBER -= 1
        if self.QUESTIONNUMBER < 1:
            self.QUESTIONNUMBER = 1
        self.textview.setText(questions[str(self.QUESTIONNUMBER)])
        self.radioA.setText(answers[self.QUESTIONNUMBER][0])
        self.radioB.setText(answers[self.QUESTIONNUMBER][1])
        self.radioC.setText(answers[self.QUESTIONNUMBER][2])
        if self.choocedAnswer[self.QUESTIONNUMBER] != 0:
            if self.choocedAnswer[self.QUESTIONNUMBER] == "A":
                self.radioA.setChecked(True)
            elif self.choocedAnswer[self.QUESTIONNUMBER] == "B":
                self.radioB.setChecked(True)
            elif self.choocedAnswer[self.QUESTIONNUMBER] == "C":
                self.radioC.setChecked(True)

    #跳转到下一题的函数
    #先判断是否为最后一题，是则统计结果，
    #调用sumscore统计原始分和标准分
    #调用conclusion分析统计结果并展示到UI
    #否则加载下一题题目与答案，展示到UI
    def runnext(self):
        self.scores[self.QUESTIONNUMBER] = self.calculate()
        if self.QUESTIONNUMBER == 187:
            self.resize(950,600)
            self.textview.clear()
            self.sumscore()
            self.conclusion()
        else:
            self.QUESTIONNUMBER += 1
            self.textview.setText(questions[str(self.QUESTIONNUMBER)])
            self.radioA.setText(answers[self.QUESTIONNUMBER][0])
            self.radioB.setText(answers[self.QUESTIONNUMBER][1])
            self.radioC.setText(answers[self.QUESTIONNUMBER][2])

            if self.choocedAnswer[self.QUESTIONNUMBER] != 0:
                if self.choocedAnswer[self.QUESTIONNUMBER] == "A":
                    self.radioA.setChecked(True)
                elif self.choocedAnswer[self.QUESTIONNUMBER] == "B":
                    self.radioB.setChecked(True)
                elif self.choocedAnswer[self.QUESTIONNUMBER] == "C":
                    self.radioC.setChecked(True)
            else:
                if self.choocedAnswer[self.QUESTIONNUMBER-1] == "A":
                    self.radioC.setChecked(True)
                    self.radioA.setChecked(True)
                elif self.choocedAnswer[self.QUESTIONNUMBER-1] == "B":
                    self.radioA.setChecked(True)
                    self.radioB.setChecked(True)
                elif self.choocedAnswer[self.QUESTIONNUMBER-1] == "C":
                    self.radioB.setChecked(True)
                    self.radioC.setChecked(True)


    #选择按钮的回调函数
    #当选择按钮被点击时，设置self.choocedAnswer为当前答案
    def runradioA(self):
        if self.radioA.isChecked() == True:
            self.choocedAnswer[self.QUESTIONNUMBER] = "A"
    def runradioB(self):
        if self.radioB.isChecked() == True:
            self.choocedAnswer[self.QUESTIONNUMBER] = "B"
    def runradioC(self):
        if self.radioC.isChecked() == True:
            self.choocedAnswer[self.QUESTIONNUMBER] = "C"

    #计算每题得分的函数
    #有两种计分方法，根据self.setA判断具体用哪一种
    def calculate(self):
        if self.QUESTIONNUMBER in self.setA:
            if self.choocedAnswer[self.QUESTIONNUMBER] == correctanswer[self.QUESTIONNUMBER]:
                return 1
            else:
                return 0
        else:
            if self.choocedAnswer[self.QUESTIONNUMBER] == correctanswer[self.QUESTIONNUMBER]:
                return 2
            elif self.choocedAnswer[self.QUESTIONNUMBER] == "B":
                return 1
            else:
                return 0

    #统计原始分并转化为标准分的函数
    # i 当前所统计的类别索引
    # sum 用于保存当前类别原始分总和
    # j 当前项的标准分
    # kindnum 用于展示各类题目编号的字符串
    # kindscore 用于展示各类题目得分以及原始分和标准分的字符串
    def sumscore(self):
        self.content.append(draw_text('姓名:'+login.getname()+' 日期:'+str(datetime.datetime.now())[:10]))
        i = 0
        scoretable = []
        for kind in characterindex:
            # 计算原始分
            scoretable.append([])
            scoretable.append([])
            sum = 0
            kindnum = "题号   "
            scoretable[-2].append("题号")
            if i < 12:
                kindscore = characterkind[i] + "     "
            else:
                kindscore = characterkind[i] + "    "
            scoretable[-1].append(characterkind[i])
            for index in kind:
                sum += self.scores[index]
                # 生成题号索引和原始分字符串
                if index < 10:
                    kindnum += str(index) + "    "
                elif index < 100:
                    kindnum += str(index) + "   "
                else:
                    kindnum += str(index) + "  "
                scoretable[-2].append(index)
                kindscore += str(self.scores[index]) + "    "
                scoretable[-1].append(self.scores[index])

            if len(kind) == 10:
                kindnum += "               "
                scoretable[-2].append('')
                scoretable[-2].append('')
                scoretable[-2].append('')
                kindscore += "               "
                scoretable[-1].append("")
                scoretable[-1].append('')
                scoretable[-1].append('')
            if characterkind[i] == "A ":
                kindnum += "原始分 标准分  性格  低  中  高"
                templist = ['原始分','标准分','性格','低','中','高']
                for x in templist:
                    scoretable[-2].append(x)
                
            # 计算标准分并添加到末尾
            j = 1
            standardscore = 0
            for section in scorerule[i]:
                if sum in section:
                    standardscore = j
                    self.standardscore.append(standardscore)
                    break
                else:
                    j += 1
            kindscore += "  "+str(sum)
            scoretable[-1].append(sum)
            if sum < 10:
                kindscore += "     "
            else:
                kindscore += "    "
            skindscore = kindscore#skindscore:用于生成TXT的string
            kindscore += str(standardscore)
            scoretable[-1].append(standardscore)
            if standardscore < 10:
                kindscore += "    "
            else:
                kindscore += "   "
            kindscore += characterkindd[i]
            scoretable[-1].append(characterkindd[i])

            if standardscore <= 3:
                kindscore += "  D       "
                scoretable[-1].append('D')
                scoretable[-1].append('')
                scoretable[-1].append('')
            elif standardscore < 8:
                kindscore += "     Z    "
                scoretable[-1].append('')
                scoretable[-1].append('Z')
                scoretable[-1].append('')
            else:
                kindscore += "         G"
                scoretable[-1].append('')
                scoretable[-1].append('')
                scoretable[-1].append('G')

            # self.scoressum[i] = sum
            self.textview.append(kindnum)
            self.textview.append(kindscore)
            skindscore += kindscore[79:]
            self.mainString += kindnum+"\n"+skindscore+"\n\n"
            i += 1
        self.textview.append(" ")
        self.content.append(draw_table(scoretable,29))

    #根据标准分分析得出结果并展示到UI
    # choocedstandard 保存选择出来的大于8和小于3的标准分
    # standardscorecopy 保存标准分数组的复制
    def conclusion(self):
        self.radioA.hide()
        self.radioB.hide()
        self.radioC.hide()
        self.formerbutton.hide()
        self.nextbutton.hide()
        self.holder.show()
        self.downloadbutton.show()
        choocedstandard = []
        
        #获取目标标准分数组
        for score in self.standardscore:
            if score <= 3 or score >= 8:
                choocedstandard.append(score)
        if len(choocedstandard) <= 1:
            sortedstandard = self.standardscore.copy()
            sortedstandard.sort()
            choocedstandard = sortedstandard[:1]+sortedstandard[15:]
        elif len(choocedstandard) > 8:
            choocedstandard.sort()
            choocedstandard = choocedstandard[:4] + choocedstandard[-4:]
        standardscorecopy = self.standardscore.copy()
        
        #输出对应性格描述
        for sum in choocedstandard:
            index = standardscorecopy.index(sum)
            standardscorecopy[index] = 40
            suitabljobstr = '' #生成PDF文件里的适合职业的string
            #self.mainstring生成TXT的字符串
            if sum <= 5:
                self.mainString += self.fomatestr(characterdiscreption[index][0])
                self.textview.append("    "+characterdiscreption[index][0])
                self.content.append(draw_text(characterdiscreption[index][0]))
            else:
                self.mainString += self.fomatestr(characterdiscreption[index][1])
                self.textview.append("    "+characterdiscreption[index][1])
                self.content.append(draw_text(characterdiscreption[index][1]))

        #输出适合职业
        self.textview.append(" ")
        self.textview.append("适合职业：")
        self.mainString +='\n'+"适合职业："+'\n'
        self.content.append(draw_little_title("适合职业："))
        standardscorecopy = self.standardscore.copy()
        for sum in choocedstandard:
            index = standardscorecopy.index(sum)
            standardscorecopy[index] = 40
            if sum <= 5:
                if suitablejob[index][0] != "":
                    self.textview.append(" " + suitablejob[index][0])
                    self.mainString +=" " + suitablejob[index][0]+'\n'
                    suitabljobstr += suitablejob[index][0] +';'
            else:
                if suitablejob[index][1] != "":
                    self.textview.append(" " + suitablejob[index][1])
                    self.mainString += " " + suitablejob[index][1]+'\n'
                    suitabljobstr += suitablejob[index][1] + ';'

        self.content.append(draw_text(suitabljobstr))

    #s:需要被格式化的string
    #lenline：被格式化后的行长度
    #fomatedstr：保存被格式化后的string
    def fomatestr(self,s:str):
        lenline = 50
        lenstr = lenline
        fomatedstr = "    "
        while lenstr < len(s)+lenline:
            fomatedstr += s[lenstr - lenline:lenstr] + '\n'
            lenstr += lenline
        return fomatedstr


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWidget()
    main = MainWidget()
    login.show()
    sys.exit(app.exec_())
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
