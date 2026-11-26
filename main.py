from PySide6 import QtCore, QtWidgets, QtGui
import sys
import numpy
import time
import backend

application = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()

windowSize = QtCore.QSize(600,700)

class BotWidget(QtWidgets.QWidget):

    def __init__(self, x:float=0, y:float=0, h:float=0, t:float=10):
        super().__init__()
        self.bot = backend.OdometerBot(x,y,h,t)
        self.setMinimumSize(windowSize.width()-50,windowSize.height()-200)
    
    def paintEvent(self, event):
        #init vars
        x = self.bot.getX()
        y = self.bot.getY()# - windowSize.height()
        h = self.bot.getHeading()
        t = self.bot.getTrackWidth()

        #paint stuff
        painter = QtGui.QPainter(self)
        # painter.begin(self)
        painter.fillRect(self.rect(), QtCore.Qt.GlobalColor.white)
        painter.translate(self.width()/2,self.height()/2)
        painter.scale(2,-2)
        #draw center
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtCore.Qt.GlobalColor.lightGray)
        painter.setPen(pen)
        painter.drawLine(0,-100,0,100)
        painter.drawLine(-100,0,100,0)
        #get points to draw
        center = QtCore.QPointF(x, (y))
        forward = QtCore.QPointF(x + t * numpy.cos(numpy.deg2rad(h)), (y + t * numpy.sin(numpy.deg2rad(h))))
        left = QtCore.QPointF(x - t/2 * numpy.sin(numpy.deg2rad(h)), (y + t/2 * numpy.cos(numpy.deg2rad(h))))
        right = QtCore.QPointF(x + t/2 * numpy.sin(numpy.deg2rad(h)), (y - t/2 * numpy.cos(numpy.deg2rad(h))))
        #draw front
        pen.setWidth(int(1+self.bot.getTrackWidth()/8))
        pen.setColor(QtCore.Qt.GlobalColor.red)
        painter.setPen(QtCore.Qt.GlobalColor.red)
        painter.setPen(pen)
        painter.drawLine(center, forward)
        #draw sides
        pen.setColor(QtCore.Qt.GlobalColor.blue)
        painter.setPen(pen)
        painter.drawLine(center, left)
        painter.drawLine(center, right)
        #draw outline
        painter.scale(0.5,-0.5)
        painter.translate(-self.width()/2,-self.height()/2)
        pen.setWidth(8)
        pen.setColor(QtCore.Qt.GlobalColor.black)
        painter.setPen(pen)
        painter.drawRect(self.rect())
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
        self.container.setContentsMargins(0,0,0,0)
        self.validator = QtGui.QDoubleValidator(-10e3,10e3,3)
        self.labelWidget = QtWidgets.QLabel(name)
        self.valueWidget = QtWidgets.QLineEdit(str(defaultValue))
        self.valueWidget.textChanged.connect(lambda: self.valueChanged.emit(self.value()))
        self.valueWidget.setValidator(self.validator)
        self.container.addWidget(self.labelWidget)
        self.container.addWidget(self.valueWidget)
    def value(self) -> float: return toFloat(self.valueWidget.text())
    def setValue(self, value:float):
        self.blockSignals(True)
        self.valueWidget.setText(f"{value:.3f}")
        self.blockSignals(False)

class BooleanField(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(bool)
    def __init__(self, trueName: str, falseName: str, value: bool = True):
        super().__init__()
        self.container = QtWidgets.QHBoxLayout(self)
        self.container.setContentsMargins(0,0,0,0)
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
container.setSpacing(8)
container.setContentsMargins(16,16,16,16)

bot = BotWidget()
bot.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
container.addWidget(bot, 1)
container.addSpacing(16)
# container.addWidget(bot, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

botSettings = QtWidgets.QHBoxLayout()
x = InputField("x")
y = InputField("y")
h = InputField("direction")
t = InputField("size")

def updateFields():
    x.setValue(bot.bot.getX())
    y.setValue(bot.bot.getY())
    h.setValue(bot.bot.getHeading())
    t.setValue(max(1e-3,bot.bot.getTrackWidth()))


resetPos = QtWidgets.QPushButton("Reset")

def reset():
    bot.bot.setPose(backend.Pose(0,0,0))
    bot.bot.setTrackWidth(12)
    updateFields()
    bot.update()
    
resetPos.clicked.connect(reset)
reset()

botSettings.addSpacing(8)
botSettings.addWidget(resetPos, 0)
botSettings.addWidget(x, 0)
botSettings.addWidget(y, 0)
botSettings.addWidget(h, 0)
botSettings.addWidget(t, 0)
botSettings.addSpacing(8)
container.addLayout(botSettings)

def updateBot():
    if(t.value()<1e-3): t.setValue(1e-3)
    bot.bot.setPose(backend.Pose(x.value(), y.value(), h.value()))
    bot.bot.setTrackWidth(t.value())
    bot.update() # redraws it

x.valueChanged.connect(updateBot)
y.valueChanged.connect(updateBot)
h.valueChanged.connect(updateBot)
t.valueChanged.connect(updateBot)

updateBot()



runSettings = QtWidgets.QHBoxLayout()
runtype = BooleanField("Run Wheels","Run Arc", True)
i1 = InputField("dL",40)
i2 = InputField("dR",20)
steps = InputField("Steps",20)
repeats = InputField("Repeat",5)

def updateRunType():
    if(runtype.value()):
        i1.labelWidget.setText("dL")
        i2.labelWidget.setText("dR")
    else:
        i1.labelWidget.setText("dH")
        i2.labelWidget.setText("avgD")


stepsLeft = 0
repeatsLeft = 0
timer = QtCore.QTimer()

def runBot_onTick():
    global stepsLeft
    global repeatsLeft
    global steps
    if(repeatsLeft <= 0): return
    if (stepsLeft <= 0):
        stepsLeft = steps.value()
        repeatsLeft -= 1

    if(runtype.value()):
        bot.bot.stepWheels(i1.value()/steps.value(), i2.value()/steps.value())
    else:
        bot.bot.stepArc(i1.value()/steps.value(), i2.value()/steps.value())
    bot.update()
    updateFields()
    stepsLeft -= 1


        
timer.setInterval(10)
timer.timeout.connect(runBot_onTick)
timer.start()

def runBot():
    # global stepsLeft
    global repeatsLeft
    global repeats
    # stepsLeft = int(steps.value())
    if(repeatsLeft == 0): repeatsLeft = int(repeats.value())
        

updateRunType()
runtype.valueChanged.connect(updateRunType)
runButton = QtWidgets.QPushButton("Run!")
runButton.setMinimumHeight(64)
runButton.setStyleSheet("""
    QPushButton
    {
        background-color: lightgreen;
        color: crimson;
        font-weight: bold;
        font-size: 32px;
        border: 4px solid teal;
    }
    QPushButton:hover
    {
        color: maroon;
        background-color: mediumseagreen
    }
    QPushButton:pressed
    {
        color: darkorange;
        background-color: mediumspringgreen
    }
""")
runButton.clicked.connect(runBot)

runSettings.addSpacing(8)
runSettings.addWidget(runtype)
runSettings.addWidget(i1)
runSettings.addWidget(i2)
runSettings.addWidget(steps)
runSettings.addWidget(repeats)
runSettings.addSpacing(8)
container.addLayout(runSettings)
container.addSpacing(8)
container.addWidget(runButton)
container.addSpacing(8)

window.setMinimumSize(windowSize)
window.resize(windowSize)
window.show()
sys.exit(application.exec())