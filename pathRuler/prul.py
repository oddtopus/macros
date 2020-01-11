#! /usr/bin/python3
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
        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setCursor(QtCore.Qt.CrossCursor)
        # layout #
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
        ##
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        # self.actionGet_reference_length = QtWidgets.QAction(self)
        # self.actionSet_unit = QtWidgets.QAction(self)
        # self.actionSet_reference = QtWidgets.QAction(self)
        self.actionSettings = QtWidgets.QAction(self)
        self.actionSettings.setText("Settings")
        self.menuActions.addAction(self.actionSettings)
        self.actionSettings.triggered.connect(self.showSettings)
        # self.menuActions.addAction(self.actionSet_unit)
        # self.actionSet_unit.triggered.connect(self.set_unit)
        # self.menuActions.addAction(self.actionSet_reference)
        # self.actionSet_reference.triggered.connect(self.set_reference)
        # self.actionSet_reference.setText("Set reference")
        # self.actionGet_reference_length.setText("Get reference length")
        self.menuActions.setTitle("Actions")
        self.menubar.addAction(self.menuActions.menuAction())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    def mouseReleaseEvent(self,event):
        if event.button()==1:
            #print("x = %s, y=%s" %(event.x(), event.y()))
            if self.ref:
              self.points.append(event.pos())
            else:
              self.points=[]
              #self.label.setText("Total Length = %.2f [%s]" %(0, self.um))
              self.refPoints.append(event.pos())
              if len(self.refPoints)>=2:
                P1,P2=self.refPoints[:2]
                self.ref=sqrt((P1.x()-P2.x())**2+(P1.y()-P2.y())**2)
                #print('Reference = %.2f pixels' %self.ref)
                self.label.setText('Reference: %.2f [pixels] = %.2f [%s]' %(self.ref,self.refL,self.um))
                self.settings.show()
              else:
                self.label.setText("Pick another one")
        elif event.button()==2:
          self.points=[]
          self.label.setText("Total Length = %.2f [%s]" %(0, self.um))
        self.update()
    # def get_reference_length(self):
        # print('get ref length')
        # self.ref=0
        # self.refPoints=[]
    # def set_reference(self):
        # self.refL=QtWidgets.QInputDialog.getDouble(self,'ref. length','Insert reference length')[0]
    # def set_unit(self):
        # self.um=QtWidgets.QInputDialog.getText(self,'unit','Insert ref. unit')[0]
    def showSettings(self):
        self.settings.show()
    def paintEvent(self,event):
        L=0
        painter=QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.red,4,QtCore.Qt.DashLine))
        if len(self.points)>1 and self.ref:
            for i in list(range(len(self.points))):
                if i:
                  P1,P2=self.points[i-1 : i+1]
                  painter.drawLine(P1,P2)#self.points[i-1],self.points[i])
                  L+=sqrt((P1.x()-P2.x())**2+(P1.y()-P2.y())**2)*self.refL/self.ref
            self.label.setText("Total Length = %.2f [%s]" %(L, self.um))
        # text = self.scene().addSimpleText('(%d, %d)' % (self.points[-1].x(), self.points[-1].y()))
        # text.setBrush(QtCore.Qt.red)
        # text.setPos(self.points[-1])

class Settings(QtWidgets.QDialog):
    def __init__(self,parent):
        super(Settings,self).__init__(parent)
        self.parent=parent
        self.resize(180, 260)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.editDist = QtWidgets.QLineEdit(self)
        self.editDist.setAlignment(QtCore.Qt.AlignCenter)
        self.editDist.setObjectName("editDist")
        self.verticalLayout.addWidget(self.editDist)
        self.label_2 = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.editUnit = QtWidgets.QLineEdit(self)
        self.editUnit.setAlignment(QtCore.Qt.AlignCenter)
        self.editUnit.setObjectName("editUnit")
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
        self.btnRef.setObjectName("btnRef")
        self.btnRef.clicked.connect(self.getRef)
        self.verticalLayout.addWidget(self.btnRef)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        # texts #
        self.setWindowTitle("Settings")
        self.label.setText("Reference distance")
        self.editDist.setText(str(self.parent.refL))
        self.label_2.setText("Unit of measure")
        self.editUnit.setText(str(self.parent.um))
        self.btnRef.setText("Get ref. length\non screen")
        # validating #
        self.editDist.setValidator(QtGui.QDoubleValidator())
    def getRef(self):
        self.parent.ref=0
        self.parent.refPoints=[]
        self.parent.refL=float(self.editDist.text())
        self.parent.um=self.editUnit.text()
        self.parent.update()
        self.parent.label.setText("Pick two points on the screen")
        self.hide()
    def accept(self):
        # super(Settings,self)
        self.parent.refL=float(self.editDist.text())
        self.parent.um=self.editUnit.text()
        super(Settings,self).accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

