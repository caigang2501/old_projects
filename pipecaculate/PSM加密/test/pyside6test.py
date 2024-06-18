# import random
# import sys

# from PySide6.QtCore import Qt, Slot
# from PySide6.QtWidgets import (QApplication, QLabel, QPushButton,
#                                QVBoxLayout, QWidget)
# # from __feature__ import snake_case, true_property


# class MyWidget(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)

#         self.hello = [
#             "Hallo Welt",
#             "你好，世界",
#             "Hei maailma",
#             "Hola Mundo",
#             "Привет мир",
#         ]

#         self.button = QPushButton("Click me!")
#         self.message = QLabel("Hello World")
#         self.message.alignment = Qt.AlignCenter

#         self.layout = QVBoxLayout(self)
#         self.layout.add_widget(self.message)
#         self.layout.add_widget(self.button)

#         # Connecting the signal
#         self.button.clicked.connect(self.magic)

#     @Slot()
#     def magic(self):
#         self.message.text = random.choice(self.hello)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     widget = MyWidget()
#     widget.show()

#     sys.exit(app.exec_())


import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
