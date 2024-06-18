import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QTableWidget,QApplication,QListWidget

class LoginWidget(QMainWindow):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)

        self.setWindowTitle("login")
        self.resize(600, 400)
        self.setCentralWidget(QWidget())
        self.main_layout = QVBoxLayout(self.centralWidget())

        # itemview = QAbstractItemView(QWidget())
        # # tableview = QTableView(itemview)
        table = QTableWidget()
        table.insertRow(2)
        self.main_layout.addWidget(table)
        listview = QListWidget()
        listview.addItems(['密密麻麻','密密麻麻','密密麻麻'])
        self.main_layout.addWidget(listview)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginWidget()
    login.show()
    sys.exit(app.exec_())