from PySide6 import QtCore, QtWidgets, QtGui
import sys
import numpy
import backend

application = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

windowSize = QtCore.QSize(600,600)

class BotWidget(QtWidgets.QWidget):

    def __init__(self, x:float, y:float, h:float, t:float):
        super().__init__()
        self.bot = backend.OdometerBot(x,y,h,t)
    
    def paintEvent(self, event):
        x = self.bot.getX()
        y = self.bot.getY() - windowSize.height()
        h = self.bot.getHeading()
        t = self.bot.getTrackWidth()
        self.resize(500,500)
        painter = QtGui.QPainter(self)
        # painter.begin(self)
        center = QtCore.QPointF(x, -(y))
        forward = QtCore.QPointF(x + t * numpy.cos(numpy.deg2rad(h)), -(y + t * numpy.sin(numpy.deg2rad(h))))
        left = QtCore.QPointF(x - t/2 * numpy.sin(numpy.deg2rad(h)), -(y + t/2 * numpy.cos(numpy.deg2rad(h))))
        right = QtCore.QPointF(x + t/2 * numpy.sin(numpy.deg2rad(h)), -(y - t/2 * numpy.cos(numpy.deg2rad(h))))
        painter.setPen(QtCore.Qt.GlobalColor.red)
        painter.drawLine(center, forward)
        painter.setPen(QtCore.Qt.GlobalColor.blue)
        painter.drawLine(center, left)
        painter.drawLine(center, right)
        # painter.end()
        return super().paintEvent(event)

def toFloat(str, default: float = 0.0):
    try:
        return float(str)
    except (ValueError, TypeError):
        return default

class InputField(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)
    def __init__(self, name: str, defaultValue: float = 0):
        super().__init__()
        self.container = QtWidgets.QHBoxLayout(self)
        self.labelWidget = QtWidgets.QLabel(name)
        self.valueWidget = QtWidgets.QLineEdit(str(defaultValue))
        self.valueWidget.textChanged.connect(lambda: self.valueChanged.emit(self.value()))
        self.container.addWidget(self.labelWidget)
        self.container.addWidget(self.valueWidget)
    def value(self) -> float: return toFloat(self.valueWidget.text())

class BooleanField(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(bool)
    def __init__(self, trueName: str, falseName: str, value: bool = True):
        super().__init__()
        self.container = QtWidgets.QHBoxLayout(self)
        self.trueName = trueName
        self.falseName = falseName
        self.labelWidget = QtWidgets.QLabel(self.trueName if value else self.falseName)
        self.valueWidget = QtWidgets.QCheckBox()
        self.valueWidget.setChecked(value)
        self.valueWidget.checkStateChanged.connect(self.onChange)
        self.container.addWidget(self.labelWidget)
        self.container.addWidget(self.valueWidget)
    def value(self) -> bool: return self.valueWidget.checkState() == QtCore.Qt.CheckState.Checked
    def onChange(self):
        self.labelWidget.setText(self.trueName if self.value() else self.falseName)
        self.valueChanged.emit(self.value())

container = QtWidgets.QVBoxLayout(window)

bot = BotWidget(20,-300,30, 12)
container.addWidget(bot, 1)

botSettings = QtWidgets.QHBoxLayout()
x = InputField("x","100")
y = InputField("y","300")
h = InputField("direction","0")
t = InputField("size","20")
botSettings.addWidget(x, 0)
botSettings.addWidget(y, 0)
botSettings.addWidget(h, 0)
botSettings.addWidget(t, 0)
container.addLayout(botSettings)

def update():
    bot.bot.setPose(backend.Pose(x.value(), y.value(), h.value()))
    bot.bot.setTrackWidth(t.value())
    bot.update() # redraws it

x.valueChanged.connect(update)
y.valueChanged.connect(update)
h.valueChanged.connect(update)
t.valueChanged.connect(update)

update()



runSettings = QtWidgets.QHBoxLayout()
runtype = BooleanField("Run Wheels","Run Arc", True)
i1 = InputField("dL",10)
i2 = InputField("dR",8)
steps = InputField("Steps",10)

def updateRunType():
    if(runtype.value()):
        i1.labelWidget.setText("dL")
        i2.labelWidget.setText("dR")
    else:
        i1.labelWidget.setText("dH")
        i2.labelWidget.setText("avgD")

def runBot():
    if(runtype.value()):
        bot.bot.runWheels(i1.value(), i2.value(), int(steps.value()))
    else:
        bot.bot.runArc(i1.value(), i2.value(), int(steps.value()))
    bot.update()

updateRunType()
runtype.valueChanged.connect(updateRunType)
runButton = QtWidgets.QPushButton("Run!")
runButton.clicked.connect(runBot)

runSettings.addWidget(runtype)
runSettings.addWidget(i1)
runSettings.addWidget(i2)
runSettings.addWidget(steps)
runSettings.addWidget(runButton)
container.addLayout(runSettings)

window.resize(windowSize)
window.show()
sys.exit(application.exec())