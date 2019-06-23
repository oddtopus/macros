__title__="FreeCAD Custom Profile"
__author__ = "oddtopus"

#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019                                                    *
#*   oddtopus                                 *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

from PySide.QtCore import *
from PySide.QtGui import *
from os.path import join,dirname,abspath
import FreeCAD, customArchProfile

pixSquare=QPixmap(join(dirname(abspath(__file__)),"square.png"))
pixT=QPixmap(join(dirname(abspath(__file__)),"T.png"))
pixU=QPixmap(join(dirname(abspath(__file__)),"U.png"))
pixH=QPixmap(join(dirname(abspath(__file__)),"H.png"))
pixL=QPixmap(join(dirname(abspath(__file__)),"L.png"))
pixZ=QPixmap(join(dirname(abspath(__file__)),"Z.png"))
# pixOmega=QPixmap(join(dirname(abspath(__file__)),"omega.png"))
# pixCircle=QPixmap(join(dirname(abspath(__file__)),"circle.png"))

sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
sizePolicy.setHorizontalStretch(0)
sizePolicy.setVerticalStretch(0)
# sizePolicy.setHeightForWidth(self.tbZ.sizePolicy().hasHeightForWidth())

class profEdit(QDialog):
  def __init__(self):
    super(profEdit,self).__init__()
    self.setWindowFlags(Qt.WindowStaysOnTopHint)
    self.setObjectName("Dialog")
    self.resize(304, 388)
    self.gridLayout_4 = QGridLayout(self)
    self.gridLayout_4.setObjectName("gridLayout_4")
    self.frameDims = QFrame(self)
    sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.frameDims.sizePolicy().hasHeightForWidth())
    self.frameDims.setSizePolicy(sizePolicy)
    self.frameDims.setMinimumSize(QSize(130, 100))
    self.frameDims.setFrameShape(QFrame.StyledPanel)
    self.frameDims.setFrameShadow(QFrame.Raised)
    self.frameDims.setObjectName("frameDims")
    self.gridLayout_2 = QGridLayout(self.frameDims)
    self.gridLayout_2.setObjectName("gridLayout_2")
    self.labH = QLabel(self.frameDims)
    self.labH.setAlignment(Qt.AlignCenter)
    self.labH.setObjectName("labH")
    self.gridLayout_2.addWidget(self.labH, 0, 0, 1, 1)
    self.editH = QLineEdit(self.frameDims)
    self.editH.setAlignment(Qt.AlignCenter)
    self.editH.setObjectName("editH")
    self.editH.setValidator(QDoubleValidator())
    self.gridLayout_2.addWidget(self.editH, 0, 1, 1, 1)
    self.labB = QLabel(self.frameDims)
    self.labB.setAlignment(Qt.AlignCenter)
    self.labB.setObjectName("labB")
    self.gridLayout_2.addWidget(self.labB, 1, 0, 1, 1)
    self.editB = QLineEdit(self.frameDims)
    self.editB.setAlignment(Qt.AlignCenter)
    self.editB.setObjectName("editB")
    self.editB.setValidator(QDoubleValidator())
    self.gridLayout_2.addWidget(self.editB, 1, 1, 1, 1)
    self.labD = QLabel(self.frameDims)
    self.labD.setAlignment(Qt.AlignCenter)
    self.labD.setObjectName("labD")
    self.gridLayout_2.addWidget(self.labD, 2, 0, 1, 1)
    self.editD = QLineEdit(self.frameDims)
    self.editD.setAlignment(Qt.AlignCenter)
    self.editD.setObjectName("editD")
    self.editD.setValidator(QDoubleValidator())
    self.gridLayout_2.addWidget(self.editD, 2, 1, 1, 1)
    self.editD.raise_()
    self.labH.raise_()
    self.editB.raise_()
    self.editH.raise_()
    self.labB.raise_()
    self.labD.raise_()
    self.gridLayout_4.addWidget(self.frameDims, 5, 0, 1, 1)
    self.cbFull = QCheckBox(self)
    self.cbFull.setObjectName("cbFull")
    self.gridLayout_4.addWidget(self.cbFull, 4, 1, 1, 1)
    self.labImg = QLabel(self)
    self.labImg.setMaximumSize(QSize(140, 140))
    self.labImg.setText("")
    self.labImg.setPixmap(QPixmap(join(dirname(abspath(__file__)),"square.png")))
    self.labImg.setScaledContents(True)
    self.labImg.setObjectName("labImg")
    self.gridLayout_4.addWidget(self.labImg, 0, 1, 1, 1)
    self.frameThk = QFrame(self)
    sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.frameThk.sizePolicy().hasHeightForWidth())
    self.frameThk.setSizePolicy(sizePolicy)
    self.frameThk.setMinimumSize(QSize(130, 100))
    self.frameThk.setFrameShape(QFrame.StyledPanel)
    self.frameThk.setFrameShadow(QFrame.Raised)
    self.frameThk.setObjectName("frameThk")
    self.gridLayout = QGridLayout(self.frameThk)
    self.gridLayout.setObjectName("gridLayout")
    self.labT1 = QLabel(self.frameThk)
    self.labT1.setAlignment(Qt.AlignCenter)
    self.labT1.setObjectName("labT1")
    self.gridLayout.addWidget(self.labT1, 0, 0, 1, 1)
    self.editT1 = QLineEdit(self.frameThk)
    self.editT1.setAlignment(Qt.AlignCenter)
    self.editT1.setObjectName("editT1")
    self.editT1.setValidator(QDoubleValidator())
    self.gridLayout.addWidget(self.editT1, 0, 1, 1, 1)
    self.labT2 = QLabel(self.frameThk)
    self.labT2.setAlignment(Qt.AlignCenter)
    self.labT2.setObjectName("labT2")
    self.gridLayout.addWidget(self.labT2, 1, 0, 1, 1)
    self.editT2 = QLineEdit(self.frameThk)
    self.editT2.setAlignment(Qt.AlignCenter)
    self.editT2.setObjectName("editT2")
    self.editT2.setValidator(QDoubleValidator())
    self.gridLayout.addWidget(self.editT2, 1, 1, 1, 1)
    self.labT3 = QLabel(self.frameThk)
    self.labT3.setAlignment(Qt.AlignCenter)
    self.labT3.setObjectName("labT3")
    self.gridLayout.addWidget(self.labT3, 2, 0, 1, 1)
    self.editT3 = QLineEdit(self.frameThk)
    self.editT3.setAlignment(Qt.AlignCenter)
    self.editT3.setObjectName("editT3")
    self.editT3.setValidator(QDoubleValidator())
    self.gridLayout.addWidget(self.editT3, 2, 1, 1, 1)
    self.gridLayout_4.addWidget(self.frameThk, 5, 1, 1, 1)
    self.lineEdit = QLineEdit(self)
    self.lineEdit.setAlignment(Qt.AlignCenter)
    self.lineEdit.setObjectName("lineEdit")
    self.gridLayout_4.addWidget(self.lineEdit, 3, 1, 1, 1)
    self.frameButtons = QFrame(self)
    sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(self.frameButtons.sizePolicy().hasHeightForWidth())
    self.frameButtons.setSizePolicy(sizePolicy)
    self.frameButtons.setMinimumSize(QSize(140, 0))
    self.frameButtons.setFrameShape(QFrame.StyledPanel)
    self.frameButtons.setFrameShadow(QFrame.Raised)
    self.frameButtons.setObjectName("frameButtons")
    self.gridLayout_3 = QGridLayout(self.frameButtons)
    self.gridLayout_3.setObjectName("gridLayout_3")
    self.tbH = QToolButton(self.frameButtons)
    self.tbH.setSizePolicy(sizePolicy)
    self.tbH.setMinimumSize(QSize(56, 56))
    self.tbH.setBaseSize(QSize(56, 56))
    self.tbH.setIconSize(QSize(48, 48))
    icon4 = QIcon()
    icon4.addPixmap(pixH, QIcon.Normal, QIcon.Off)
    self.tbH.setIcon(icon4)
    self.tbH.setObjectName("tbH")
    self.gridLayout_3.addWidget(self.tbH, 3, 0, 1, 1)
    self.tbSquare = QToolButton(self.frameButtons)
    self.tbSquare.setSizePolicy(sizePolicy)
    self.tbSquare.setMinimumSize(QSize(56, 56))
    self.tbSquare.setBaseSize(QSize(56, 56))
    icon = QIcon()
    icon.addPixmap(QPixmap(join(dirname(abspath(__file__)),"square.png")), QIcon.Normal, QIcon.Off)
    self.tbSquare.setIcon(icon)
    self.tbSquare.setIconSize(QSize(48, 48))
    self.tbSquare.setObjectName("tbSquare")
    self.gridLayout_3.addWidget(self.tbSquare, 0, 0, 2, 1)
    self.tbZ = QToolButton(self.frameButtons)
    self.tbZ.setSizePolicy(sizePolicy)
    self.tbZ.setMinimumSize(QSize(56, 56))
    self.tbZ.setBaseSize(QSize(56, 56))
    icon1 = QIcon()
    icon1.addPixmap(pixZ, QIcon.Normal, QIcon.Off)
    self.tbZ.setIcon(icon1)
    self.tbZ.setIconSize(QSize(48, 48))
    self.tbZ.setObjectName("tbZ")
    self.gridLayout_3.addWidget(self.tbZ, 0, 1, 2, 1)
    self.tbCircle = QToolButton(self.frameButtons)    #TO DELETE
    self.tbCircle.setSizePolicy(sizePolicy)
    self.tbCircle.setMinimumSize(QSize(56, 56))
    self.tbCircle.setBaseSize(QSize(56, 56))
    # # icon1 = QIcon()
    # icon1.addPixmap(pixCircle, QIcon.Normal, QIcon.Off)
    # self.tbCircle.setIcon(icon1)
    self.tbCircle.setIconSize(QSize(48, 48))
    self.tbCircle.setObjectName("tbCircle")
    self.gridLayout_3.addWidget(self.tbCircle, 4, 0, 1, 1)
    self.tbOmega = QToolButton(self.frameButtons)     #TODO
    self.tbOmega.setSizePolicy(sizePolicy)
    self.tbOmega.setMinimumSize(QSize(56, 56))
    self.tbOmega.setBaseSize(QSize(56, 56))
    self.tbOmega.setIconSize(QSize(48, 48))
    self.tbOmega.setObjectName("tbOmega")
    self.gridLayout_3.addWidget(self.tbOmega, 4, 1, 1, 1)
    self.tbT = QToolButton(self.frameButtons)
    self.tbT.setSizePolicy(sizePolicy)
    self.tbT.setMinimumSize(QSize(56, 56))
    self.tbT.setBaseSize(QSize(56, 56))
    icon2 = QIcon()
    icon2.addPixmap(QPixmap(join(dirname(abspath(__file__)),"T.png")), QIcon.Normal, QIcon.Off)
    self.tbT.setIcon(icon2)
    self.tbT.setIconSize(QSize(48, 48))
    self.tbT.setObjectName("tbT")
    self.gridLayout_3.addWidget(self.tbT, 2, 0, 1, 1)
    self.tbL = QToolButton(self.frameButtons)
    self.tbL.setSizePolicy(sizePolicy)
    self.tbL.setMinimumSize(QSize(56, 56))
    self.tbL.setBaseSize(QSize(56, 56))
    self.tbL.setIconSize(QSize(48, 48))
    icon5 = QIcon()
    icon5.addPixmap(pixL, QIcon.Normal, QIcon.Off)
    self.tbL.setIcon(icon5)
    self.tbL.setObjectName("tbL")
    self.gridLayout_3.addWidget(self.tbL, 3, 1, 1, 1)
    self.tbU = QToolButton(self.frameButtons)
    self.tbU.setSizePolicy(sizePolicy)
    self.tbU.setMinimumSize(QSize(56, 56))
    self.tbU.setBaseSize(QSize(56, 56))
    icon3 = QIcon()
    icon3.addPixmap(QPixmap(join(dirname(abspath(__file__)),"U.png")), QIcon.Normal, QIcon.Off)
    self.tbU.setIcon(icon3)
    self.tbU.setIconSize(QSize(48, 48))
    self.tbU.setObjectName("tbU")
    self.gridLayout_3.addWidget(self.tbU, 2, 1, 1, 1)
    self.gridLayout_4.addWidget(self.frameButtons, 0, 0, 5, 1)
    spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    self.gridLayout_4.addItem(spacerItem, 2, 1, 1, 1)
    self.btn1 = QPushButton(self)
    self.btn1.setObjectName("btn1")
    self.gridLayout_4.addWidget(self.btn1, 1, 1, 1, 1)
    ###
    self.retranslateUi(self)
    ###
    QMetaObject.connectSlotsByName(self)
    self.setTabOrder(self.lineEdit, self.cbFull)
    self.setTabOrder(self.cbFull, self.tbSquare)
    # self.setTabOrder(self.tbSquare, self.tbCircle)
    # self.setTabOrder(self.tbCircle, self.tbT)
    self.setTabOrder(self.tbT, self.tbU)
    self.setTabOrder(self.tbU, self.tbH)
    self.setTabOrder(self.tbH, self.tbL)
    self.setTabOrder(self.tbL, self.tbZ)
    self.setTabOrder(self.tbZ, self.tbOmega)
    self.setTabOrder(self.tbOmega, self.editD)
    self.setTabOrder(self.editD, self.editH)
    self.setTabOrder(self.editH, self.editB)
    self.setTabOrder(self.editB, self.editT1)
    self.setTabOrder(self.editT1, self.editT2)
    self.setTabOrder(self.editT2, self.editT3)
    self.setTabOrder(self.editT3, self.btn1)
    ###
    self.editH.setText('100')
    self.editB.setText('50')
    self.editD.setText('50')
    self.editT1.setText('5')
    self.editT2.setText('10')
    self.editT3.setText('10')
    self.type="RH"
    self.label='Square_tube'
    self.btn1.clicked.connect(self.draw)
    self.cbFull.stateChanged.connect(lambda: self.setProfile('square'))
    self.editB.editingFinished.connect(lambda: self.editD.setText(self.editB.text()))
    self.editT2.editingFinished.connect(lambda: self.editT3.setText(self.editT2.text()))
    self.tbSquare.clicked.connect(lambda: self.setProfile('square'))
    self.tbT.clicked.connect(lambda: self.setProfile('T'))
    self.tbU.clicked.connect(lambda: self.setProfile('U'))
    self.tbH.clicked.connect(lambda: self.setProfile('H'))
    self.tbL.clicked.connect(lambda: self.setProfile('L'))
    self.tbZ.clicked.connect(lambda: self.setProfile('Z'))
    #self.tbOmega.clicked.connect(lambda: self.setProfile('omega'))
    #self.cbFull.[].connect(lambda: setProfile('switchFull')
  def setProfile(self, typeS):
    if typeS=='square':
      self.labImg.setPixmap(pixSquare)
      if not self.cbFull.isChecked():
        self.type="RH"
        self.label="Square_tube"
      else: 
        self.type="R"
        self.label="Square"
    elif typeS=='T':
      self.labImg.setPixmap(pixT)
      self.type="T"
      self.label="T-profile"
    elif typeS=='U':
      self.labImg.setPixmap(pixU)
      self.type="U"
      self.label="U-profile"
    elif typeS=='H':
      self.labImg.setPixmap(pixH)
      self.type="H"
      self.label="H-profile"
    elif typeS=='L':
      self.labImg.setPixmap(pixL)
      self.type="L"
      self.label="L-profile"
    elif typeS=='Z':
      self.labImg.setPixmap(pixZ)
      self.type="Z"
      self.label="Z-profile"
    print(self.type, self.label)
  def draw(self):
    D, H, B, t1, t2, t3 = float(self.editD.text()),\
                          float(self.editH.text()),\
                          float(self.editB.text()),\
                          float(self.editT1.text()),\
                          float(self.editT2.text()),\
                          float(self.editT3.text())
    if not self.lineEdit.text(): label=self.label
    else: label= self.lineEdit.text()
    # verify dims according type
    if self.type=='RH'and t2<H/2 and t1<B/2:
      customArchProfile.doProfile(self.type,label,[B,H,t1,t2])
    elif self.type=='R':
      customArchProfile.doProfile(self.type,label,[B,H])
    elif self.type=='H':
      pass
    elif self.type=='U' and t2<H and t1<B/2:
      customArchProfile.doProfile(self.type,label,[B,H,t2,t1])
    elif self.type=='L' and t2<H and t1<B:
      customArchProfile.doProfile(self.type,label,[B,H,t1,t2])
    elif self.type=='T' and t2<H and t1<B:
      customArchProfile.doProfile(self.type,label,[B,H,t1,t2])
    elif self.type=='Z'and t2<H/2 and t1<B*2:
      customArchProfile.doProfile(self.type,label,[B,H,t1,t2])
    elif self.type=='CC':
      pass
    FreeCAD.ActiveDocument.recompute()
    FreeCAD.ActiveDocument.recompute()
  def retranslateUi(self, Dialog):
    _translate = QCoreApplication.translate
    Dialog.setWindowTitle(_translate("Dialog", "Beams profile editor"))
    self.labD.setText(_translate("Dialog", "D"))
    self.labH.setText(_translate("Dialog", "H"))
    self.labB.setText(_translate("Dialog", "B"))
    self.cbFull.setText(_translate("Dialog", "Full section"))
    self.labT1.setText(_translate("Dialog", "t1"))
    self.labT2.setText(_translate("Dialog", "t2"))
    self.labT3.setText(_translate("Dialog", "t3"))
    self.lineEdit.setPlaceholderText(_translate("Dialog", "<name>"))
    self.tbH.setText(_translate("Dialog", "..."))
    self.tbSquare.setText(_translate("Dialog", "..."))
    # self.tbCircle.setText(_translate("Dialog", "..."))
    self.tbZ.setText(_translate("Dialog", "..."))
    self.tbOmega.setText(_translate("Dialog", "..."))
    self.tbT.setText(_translate("Dialog", "..."))
    self.tbL.setText(_translate("Dialog", "..."))
    self.tbU.setText(_translate("Dialog", "..."))
    self.btn1.setText(_translate("Dialog", "Insert profile"))

form=profEdit()
form.show()
