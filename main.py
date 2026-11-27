from PySide6 import QtCore, QtWidgets, QtGui
import sys
import time
import backend
from widgets import BotWidget, FloatField, IntField, BooleanField

application = QtWidgets.QApplication(sys.argv)
windowSize = QtCore.QSize(600,700)

stepsLeft = 0
repeatsLeft = 0

bot = BotWidget()
bot.setMinimumSize(windowSize.width()-50,windowSize.height()-200)
bot.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
# container.addWidget(bot, 1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

x = FloatField("x")
y = FloatField("y")
h = FloatField("direction")
t = FloatField("size", minimum=1e-3, stepSize=1)
def updateFields():
    x.setValue(bot.bot.getX())
    y.setValue(bot.bot.getY())
    h.setValue(bot.bot.getHeading())
    t.setValue(max(1e-3,bot.bot.getTrackWidth()))
def updateBot():
    if(t.value()<1e-3): t.setValue(1e-3)
    bot.bot.setPose(backend.Pose(x.value(), y.value(), h.value()))
    bot.bot.setTrackWidth(t.value())
    bot.update() # redraws it
x.valueChanged.connect(updateBot)
y.valueChanged.connect(updateBot)
h.valueChanged.connect(updateBot)
t.valueChanged.connect(updateBot)

resetPos = QtWidgets.QPushButton("Reset")
def reset():
    global repeatsLeft
    global stepsLeft
    bot.bot.setPose(backend.Pose(0,0,0))
    bot.bot.setTrackWidth(12)
    updateFields()
    bot.update()
    repeatsLeft = 0
    stepsLeft = 0
resetPos.clicked.connect(reset)
reset()


runtype = BooleanField("Run Wheels","Run Arc", True)
i1 = FloatField("dL",40)
i2 = FloatField("dR",20)
def updateRunType():
    if(runtype.value()):
        i1.labelWidget.setText("dL")
        i2.labelWidget.setText("dR")
    else:
        i1.labelWidget.setText("dH")
        i2.labelWidget.setText("avgD")
runtype.valueChanged.connect(updateRunType)
updateRunType()

steps = IntField("Steps",20,1)
repeats = IntField("Repeat",5,1)
def runBot():
    # global stepsLeft
    global repeatsLeft
    global repeats
    # stepsLeft = int(steps.value())
    if(repeatsLeft == 0): repeatsLeft = int(repeats.value())
def runBot_onTick(): # this method is triggered by the timer every 10 ms. If there are steps left or it needs to repeat, it will do so.
    global stepsLeft
    global repeatsLeft
    global steps
    if(repeatsLeft <= 0 and stepsLeft <= 0): return
    if(runtype.value()):
        bot.bot.stepWheels(i1.value()/steps.value(), i2.value()/steps.value())
    else:
        bot.bot.stepArc(i1.value()/steps.value(), i2.value()/steps.value())
    bot.update()
    updateFields()
    # print(repeats.value() * steps.value() - (repeatsLeft*steps.value() + stepsLeft))
    stepsLeft -= 1
    if (repeatsLeft > 0 and stepsLeft <= 0):
        stepsLeft = int(steps.value())
        repeatsLeft -= 1
timer = QtCore.QTimer()
timer.setInterval(10)
timer.timeout.connect(runBot_onTick)
timer.start()

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

botSettings = QtWidgets.QHBoxLayout()
botSettings.addSpacing(8)
botSettings.addWidget(resetPos, 0)
botSettings.addWidget(x, 0)
botSettings.addWidget(y, 0)
botSettings.addWidget(h, 0)
botSettings.addWidget(t, 0)
botSettings.addSpacing(8)

runSettings = QtWidgets.QHBoxLayout()
runSettings.addSpacing(8)
runSettings.addWidget(runtype)
runSettings.addWidget(i1)
runSettings.addWidget(i2)
runSettings.addWidget(steps)
runSettings.addWidget(repeats)
runSettings.addSpacing(8)

window = QtWidgets.QWidget()
container = QtWidgets.QVBoxLayout(window)
container.setSpacing(8)
container.setContentsMargins(16,16,16,16)
container.addWidget(bot, 1)
container.addSpacing(16)
container.addLayout(botSettings)
container.addLayout(runSettings)
container.addSpacing(8)
container.addWidget(runButton)
container.addSpacing(8)

window.setMinimumSize(windowSize)
window.resize(windowSize)
window.show()
sys.exit(application.exec())