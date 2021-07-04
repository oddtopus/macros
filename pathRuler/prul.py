#! /usr/bin/python3

# copyright 2020
# licence LGPL3 (https://github.com/oddtopus/macros/LICENSE

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from math import sqrt

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow,self).__init__()
        self.points=list()
        self.um='pixels'
        self.refL=1 #units
        self.ref=1 #pixels
        self.pathL=0
        self.settings=Settings(self)
        self.setWindowTitle("Path-ruler")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setCursor(QtCore.Qt.CrossCursor)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setStyleSheet("QLabel{background-color:yellow;color=black}")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("Total Length = --- [%s]" %self.um)
        self.verticalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.label)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        self.actionSettings = QtWidgets.QAction(self)
        self.actionSettings.setText("Settings")
        self.menuActions.addAction(self.actionSettings)
        self.actionSettings.triggered.connect(self.settings.show)
        self.menuActions.setTitle("Actions")
        self.menubar.addAction(self.menuActions.menuAction())
        if sys.platform.startswith('win'):
          self.setWindowOpacity(0.6)
        else:
          self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    def mouseReleaseEvent(self,event):
        if event.button()==1:
            if self.ref:
              self.points.append(event.pos())
            else:
              self.points=[]
              self.refPoints.append(event.pos())
              if len(self.refPoints)>=2:
                P1,P2=self.refPoints[:2]
                self.ref=sqrt((P1.x()-P2.x())**2+(P1.y()-P2.y())**2)
                self.label.setText('Reference: %.2f [pixels] = %.2f [%s]' %(self.ref,self.refL,self.um))
                self.settings.show()
              else:
                self.label.setText("Pick another one")
        elif event.button()==2:
          self.points=[]
          self.label.setText("Total Length = %.2f [%s]" %(0, self.um))
        self.update()
    def getRef(self,refL,um):
        self.ref=0
        self.refPoints=[]
        self.refL=refL
        self.um=um 
        self.update()
        self.label.setText("Pick two points on the screen")
    def writeSettings(self,refL,um):
        self.refL=refL
        self.um=um
    def paintEvent(self,event):
        L=0
        painter=QtGui.QPainter(self)
        if len(self.points)>1 and self.ref:
            for i in list(range(len(self.points))):
                if i:
                  P1,P2=self.points[i-1 : i+1]
                  painter.setPen(QtGui.QPen(QtCore.Qt.red,4,QtCore.Qt.DashLine))
                  painter.drawLine(P1,P2)
                  painter.setPen(QtGui.QPen(QtCore.Qt.yellow,1,QtCore.Qt.DotLine))
                  painter.drawLine(P1,QtCore.QPoint(P1.x(),P2.y()))
                  painter.drawLine(P1,QtCore.QPoint(P2.x(),P1.y()))
                  L+=sqrt((P1.x()-P2.x())**2+(P1.y()-P2.y())**2)*self.refL/self.ref
                  dx=(P2.x()-P1.x())*self.refL/self.ref
                  dy=(P1.y()-P2.y())*self.refL/self.ref
            self.label.setText("Total Length = %.2f [%s] - Delta x-y = %.1f,%.1f" %(L, self.um, dx, dy))

class Settings(QtWidgets.QDialog):
    def __init__(self,parent):
        super(Settings,self).__init__(parent)
        self.parent=parent
        self.resize(180, 260)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label)
        self.editDist = QtWidgets.QLineEdit(self)
        self.editDist.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.editDist)
        self.label_2 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.label_2)
        self.editUnit = QtWidgets.QLineEdit(self)
        self.editUnit.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.editUnit)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnRef = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnRef.sizePolicy().hasHeightForWidth())
        self.btnRef.setSizePolicy(sizePolicy)
        self.btnRef.setMaximumSize(QtCore.QSize(16777215, 60))
        self.btnRef.clicked.connect(self.getRef)
        self.verticalLayout.addWidget(self.btnRef)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.setWindowTitle("Settings")
        self.label.setText("Reference distance")
        self.editDist.setText(str(self.parent.refL))
        self.label_2.setText("Unit of measure")
        self.editUnit.setText(str(self.parent.um))
        self.btnRef.setText("Get ref. length\non screen")
        self.editDist.setValidator(QtGui.QDoubleValidator())
    def getRef(self):
        self.parent.getRef(float(self.editDist.text()),self.editUnit.text())
        self.hide()
    def accept(self):
        self.parent.writeSettings(float(self.editDist.text()),self.editUnit.text())
        super(Settings,self).accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

