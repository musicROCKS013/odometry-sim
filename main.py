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
# bot.setMinimumSize(windowSize.width()-50,windowSize.height()-200)
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

resetPos = QtWidgets.QPushButton("Reset")
resetPos.setStyleSheet("""
                            background-color: indianRed;
                            color: white;
                            font-weight: bold;
                        """)
def reset():
    global repeatsLeft, stepsLeft
    bot.bot.setPose(backend.Pose(0,0,0))
    bot.bot.setTrackWidth(12)
    updateFields()
    bot.update()
    repeatsLeft = 0
    stepsLeft = 0
resetPos.clicked.connect(reset)
reset()


# runtype = BooleanField("Run Wheels","Run Arc", True)
runtypeWidget = QtWidgets.QPushButton()
runtype = True # True = Run Wheels / False = Run Arc
i1 = FloatField("dL",40)
i2 = FloatField("dR",20)

def updateBot():
    global bot, x, y, h, t, runtype, i1, i2
    if(t.value()<1e-3): t.setValue(1e-3)
    bot.bot.setPose(backend.Pose(x.value(), y.value(), h.value()))
    bot.bot.setTrackWidth(t.value())
    if(runtype):
        bot.protrusionL = i1.value()
        bot.protrusionR = i2.value()
    else:
        bot.protrusionL = i2.value() - i1.value() * t.value()/2 # double dL = avgD - dH * trackWidth/2;
        bot.protrusionR = i2.value() + i1.value() * t.value()/2 # double dR = avgD + dH * trackWidth/2;
    bot.update() # redraws it

x.valueChanged.connect(updateBot)
y.valueChanged.connect(updateBot)
h.valueChanged.connect(updateBot)
t.valueChanged.connect(updateBot)
i1.valueChanged.connect(updateBot)
i2.valueChanged.connect(updateBot)
updateBot()

def toggle():
    global runtype, runtypeWidget
    runtype = not runtype
    if(runtype):
        runtypeWidget.setText("Run Wheels")
        runtypeWidget.setStyleSheet("""
                background-color: green;
                color: lightgreen;
                font-weight: bold;
            """)
        i1.labelWidget.setText("dL")
        i2.labelWidget.setText("dR")
    else:
        runtypeWidget.setText("Run Arc")
        runtypeWidget.setStyleSheet("""
                background-color: firebrick;
                color: mistyrose;
                font-weight: bold;
            """)
        i1.labelWidget.setText("dH")
        i2.labelWidget.setText("avgD")
    updateBot()
runtypeWidget.clicked.connect(toggle)
runtype = not True
toggle() #runtime is now true


steps = IntField("Steps",20,1)
repeats = IntField("Repeat",1,1)
def runBot():
    # global stepsLeft
    global repeatsLeft, repeats
    # stepsLeft = int(steps.value())
    if(repeatsLeft == 0): repeatsLeft = int(repeats.value())
def runBot_onTick(): # this method is triggered by the timer every 10 ms. If there are steps left or it needs to repeat, it will do so.
    global stepsLeft, repeatsLeft, steps, runtype
    if(repeatsLeft <= 0 and stepsLeft <= 0): return
    
    stepsLeft -= 1
    if (repeatsLeft > 0 and stepsLeft <= 0):
        stepsLeft = int(steps.value()) - 1
        repeatsLeft -= 1

    if(runtype):
        bot.bot.stepWheels(i1.value()/steps.value(), i2.value()/steps.value())
    else:
        bot.bot.stepArc(i1.value()/steps.value(), i2.value()/steps.value())
    bot.update()
    updateFields()
    
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
runButton.setSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Maximum)
runButton.setMinimumWidth(120)
runButton.clicked.connect(runBot)

botSettings = QtWidgets.QVBoxLayout()
botSettings.addSpacing(8)
botSettings.addWidget(x, 0)
botSettings.addWidget(y, 0)
botSettings.addWidget(h, 0)
botSettings.addWidget(t, 0)
botSettings.addWidget(resetPos, 0)
# botSettings.addSpacing(8)
botSettings.addStretch()

runSettings = QtWidgets.QVBoxLayout()
runSettings.addSpacing(8)
rs1 = QtWidgets.QHBoxLayout()
rs1.addWidget(runtypeWidget)
rs1.addWidget(i1)
rs1.addWidget(i2)
runSettings.addLayout(rs1)
rs2 = QtWidgets.QHBoxLayout()
rs2.addWidget(steps)
rs2.addWidget(repeats)
runSettings.addLayout(rs2)
# runSettings.addSpacing(8)

upperContainer = QtWidgets.QHBoxLayout()
# maincontainer.setSpacing(8)
# uppderContainer.setContentsMargins(16,16,16,16)
upperContainer.addWidget(bot, 1)
# maincontainer.addSpacing(16)
sideContainer = QtWidgets.QVBoxLayout()
sideContainer.addLayout(botSettings)
upperContainer.addLayout(sideContainer)

lowerContainer = QtWidgets.QHBoxLayout()
# lowerContainer.setContentsMargins(16,16,16,16)
lowerContainer.addLayout(runSettings)
lowerContainer.addWidget(runButton)
# lowerContainer.addSpacing(8)
lowerContainer.addSpacing(8)


window = QtWidgets.QWidget()
mainContainer = QtWidgets.QVBoxLayout(window)
mainContainer.addLayout(upperContainer)
mainContainer.addLayout(lowerContainer)

# window.setMinimumSize(windowSize)
window.resize(windowSize)
window.show()
sys.exit(application.exec())