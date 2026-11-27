from PySide6 import QtCore, QtWidgets, QtGui
import numpy
import backend


class BotWidget(QtWidgets.QWidget):

    def __init__(self, x:float=0, y:float=0, h:float=0, t:float=10):
        super().__init__()
        self.bot = backend.OdometerBot(x,y,h,t)
        self.protrusionL = 0
        self.protrusionR = 0
    
    def paintEvent(self, event):
        #init vars
        x = self.bot.getX()
        y = self.bot.getY()# - windowSize.height()
        h = self.bot.getHeading()
        t = self.bot.getTrackWidth()

        #paint stuff
        painter = QtGui.QPainter(self)
        # painter.begin(self)
        painter.fillRect(self.rect(), "#FFFFFF") # background
        painter.translate(self.width()/2,self.height()/2)
        painter.scale(2,-2)
        #draw center
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor("#7DCCEC") # center cross at 0,0
        painter.setPen(pen)
        painter.drawLine(0,-self.height()/4+10,0,self.height()/4-10)
        painter.drawLine(-self.width()/4+10,0,self.width()/4-10,0)
        #get points to draw
        # center = QtCore.QPointF(x, (y))
        # forward = QtCore.QPointF(x + t * numpy.cos(numpy.deg2rad(h)), (y + t * numpy.sin(numpy.deg2rad(h))))
        # left = QtCore.QPointF(x - t/2 * numpy.sin(numpy.deg2rad(h)), (y + t/2 * numpy.cos(numpy.deg2rad(h))))
        # right = QtCore.QPointF(x + t/2 * numpy.sin(numpy.deg2rad(h)), (y - t/2 * numpy.cos(numpy.deg2rad(h))))

        center = QtCore.QPointF(self.bot.getX(),self.bot.getY())
        forward = QtCore.QPointF(x + t * numpy.cos(numpy.deg2rad(h)), (y + t * numpy.sin(numpy.deg2rad(h))))
        left = QtCore.QPointF(self.bot.getXL(),self.bot.getYL())
        leftD = QtCore.QPointF(self.bot.getXL() + self.protrusionL * numpy.cos(numpy.deg2rad(h)),self.bot.getYL() + self.protrusionL * numpy.sin(numpy.deg2rad(h)))
        right = QtCore.QPointF(self.bot.getXR(),self.bot.getYR())
        rightD = QtCore.QPointF(self.bot.getXR() + self.protrusionR * numpy.cos(numpy.deg2rad(h)),self.bot.getYR() + self.protrusionR * numpy.sin(numpy.deg2rad(h)))

        #draw protrusions
        pen.setColor("#827CF1") # protrusions
        pen.setWidth(int(1+self.bot.getTrackWidth()/64))
        painter.setPen(pen)
        painter.drawLine(left, leftD)
        painter.drawLine(right, rightD)
        #draw front
        pen.setWidth(int(2+self.bot.getTrackWidth()/16))
        pen.setColor("#F45C5C") # front
        painter.setPen(pen)
        painter.drawLine(center, forward)
        #draw sides
        pen.setColor("#F41D1D") # sides
        painter.setPen(pen)
        painter.drawLine(center, left)
        painter.drawLine(center, right)
        #draw outline
        pen.setWidth(8)
        painter.scale(0.5,-0.5)
        painter.translate(-self.width()/2,-self.height()/2)
        pen.setWidth(8)
        pen.setColor("gray") # outline
        painter.setPen(pen)
        painter.drawRect(self.rect())
        # painter.end()
        return super().paintEvent(event)


class FloatField(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)
    def __init__(self, name: str, defaultValue: float = 0, minimum: float = -999, maximum: float = 999, stepSize: float = 10):
        super().__init__()
        self.container = QtWidgets.QHBoxLayout(self)
        self.container.setContentsMargins(0,0,0,0)
        
        self.labelWidget = QtWidgets.QLabel(name)
        
        self.valueWidget = QtWidgets.QDoubleSpinBox(minimum=minimum,maximum=maximum)
        self.valueWidget.setValue(defaultValue)
        self.valueWidget.setSingleStep(stepSize)
        self.valueWidget.valueChanged.connect(lambda: self.valueChanged.emit(self.value()))
        
        self.labelWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,QtWidgets.QSizePolicy.Policy.Fixed)
        self.valueWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Fixed)
        
        self.container.addWidget(self.labelWidget)
        self.container.addWidget(self.valueWidget)
    def value(self) -> float: return self.valueWidget.value()
    def setValue(self, value:float):
        self.blockSignals(True)
        self.valueWidget.setValue(value)
        self.blockSignals(False)

class IntField(QtWidgets.QWidget):
    valueChanged = QtCore.Signal(float)
    def __init__(self, name: str, default: int = 0, minimum: int = 0, maximum: int = 999, stepSize: int = 10):
        super().__init__()
        self.container = QtWidgets.QHBoxLayout(self)
        self.container.setContentsMargins(0,0,0,0)
        
        
        self.labelWidget = QtWidgets.QLabel(name)
        
        self.valueWidget = QtWidgets.QSpinBox(minimum=minimum, maximum=maximum)
        self.valueWidget.setValue(default)
        self.valueWidget.setSingleStep(stepSize)
        self.valueWidget.valueChanged.connect(lambda: self.valueChanged.emit(self.value()))
        
        self.labelWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,QtWidgets.QSizePolicy.Policy.Fixed)
        self.valueWidget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,QtWidgets.QSizePolicy.Policy.Fixed)
        
        self.container.addWidget(self.labelWidget)
        self.container.addWidget(self.valueWidget)
    def value(self) -> int: return self.valueWidget.value()
    def setValue(self, value:int):
        self.blockSignals(True)
        self.valueWidget.setValue(value)
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


def toFloat(str, default: float = 0.0):
    try:
        return float(str)
    except (ValueError, TypeError):
        return default