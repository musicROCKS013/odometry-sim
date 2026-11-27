from PySide6 import QtCore, QtWidgets, QtGui
import numpy
import backend


class BotWidget(QtWidgets.QWidget):

    def __init__(self, x:float=0, y:float=0, h:float=0, t:float=10):
        super().__init__()
        self.bot = backend.OdometerBot(x,y,h,t)
    
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


def toFloat(str, default: float = 0.0):
    try:
        return float(str)
    except (ValueError, TypeError):
        return default