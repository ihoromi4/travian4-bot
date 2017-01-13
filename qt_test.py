import sys
from PyQt5 import QtCore, QtGui, QtWidgets

import guilib

app = QtWidgets.QApplication(sys.argv)

win = QtWidgets.QWidget()
win.setWindowTitle('Qt Win')
win.resize(300, 70)

label = QtWidgets.QLabel('<center>Hello!</center>')
btn_quit = QtWidgets.QPushButton('&Close')

vbox = QtWidgets.QVBoxLayout()
vbox.addWidget(label)
vbox.addWidget(btn_quit)

win.setLayout(vbox)

win.show()

sys.exit(app.exec())
