from PySide6 import QtCore, QtWidgets, QtGui
import sys


application = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

container = QtWidgets.QVBoxLayout(window)

label = QtWidgets.QLabel("thingy goes here")

container.addWidget(label)

window.resize(300,200)
window.show()
sys.exit(application.exec())