import os
import sys
from PyQt5.QtWidgets import QApplication,QMessageBox,QMainWindow


class ActivationWidget(QMainWindow):
    def __init__(self, parent=None):
        super(ActivationWidget, self).__init__(parent)
    def get_macaddress():
        if sys.platform == "win32":
            QMessageBox.warning(
                    None,
                    '提示',
                    f'win32:{sys.platform}') 
        else:
            QMessageBox.warning(
                    None,
                    '提示',
                    f'else:{sys.platform}')  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    if sys.platform == "win32":
            QMessageBox.warning(
                    None,
                    '提示',
                    f'win32:{sys.platform}') 
    else:
        QMessageBox.warning(
                None,
                '提示',
                f'else:{sys.platform}')
    sys.exit(app.exec_())