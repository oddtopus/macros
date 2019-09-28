#****************************************************************************
#*                                                                          *
#*   An anastruct's frontend for FreeCAD                                    *
#*   Requires libraries dodo, anastruct and a release of FC with Py3/Qt5    *
#*   Copyright (c) 2019 Riccardo Treu LGPL                                  *
#*                                                                          *
#*   For anastruct, Copyright 2018, Ritchie Vink                                                        *
#*   https://github.com/ritchie46                                                                       *
#*                                                                          *
#*   This program is free software; you can redistribute it and/or modify   *
#*   it under the terms of the GNU Lesser General Public License (LGPL)     *
#*   as published by the Free Software Foundation; either version 2 of      *
#*   the License, or (at your option) any later version.                    *
#*   for detail see the LICENCE text file.                                  *
#*                                                                          *
#*   This program is distributed in the hope that it will be useful,        *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of         *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
#*   GNU Library General Public License for more details.                   *
#*                                                                          *
#*   You should have received a copy of the GNU Library General Public      *
#*   License along with this program; if not, write to the Free Software    *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307   *
#*   USA                                                                    *
#*                                                                          *
#****************************************************************************

from anastruct import SystemElements
import FreeCAD
E=2.1e11 # N/m2 --- steel
X=FreeCAD.Vector(1,0,0)

# Form implementation generated from reading ui file 'anastruct3.ui'
# Created by: PyQt5 UI code generator 5.10.1
from PySide import QtCore, QtGui#, QtGui
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        # section tab
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.tab)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.bGO = QtGui.QPushButton(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bGO.sizePolicy().hasHeightForWidth())
        self.bGO.setSizePolicy(sizePolicy)
        self.bGO.setObjectName("bGO")
        self.gridLayout.addWidget(self.bGO,  2, 0, 1, 1)
        self.editI = QtGui.QLineEdit(self.tab)
        self.editI.setObjectName("editI")
        self.gridLayout_2.addWidget(self.editI, 5, 0, 1, 1)
        self.editA = QtGui.QLineEdit(self.tab)
        self.editA.setObjectName("editA")
        self.gridLayout_2.addWidget(self.editA, 3, 0, 1, 1)
        self.editE = QtGui.QLineEdit(self.tab)
        self.editE.setObjectName("editE")
        self.gridLayout_2.addWidget(self.editE, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 6, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        # loads tab
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.table = QtGui.QTableWidget(self.tab_2)
        self.table.setObjectName("table")
        self.table.setColumnCount(2)
        self.table.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.table, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        #nodes tab
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtGui.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.table_2 = QtGui.QTableWidget(self.tab_3)
        self.table_2.setObjectName("table_2")
        self.table_2.setColumnCount(2)
        self.table_2.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.table_2.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_2.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_2.setHorizontalHeaderItem(1, item)
        self.table_2.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_4.addWidget(self.table_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 0, 0, 1, 2)
        self.comboBox.currentIndexChanged['int'].connect(redraw)#self.table.clear)
        # retranslate
        Dialog.setWindowTitle("anastruct / fc demo")
        self.label.setText("Young modulus (N/m2)")
        self.bGO.setText("GO")
        self.editI.setPlaceholderText("section Inertia ()")
        self.editA.setPlaceholderText("section area (m2)")
        self.editE.setPlaceholderText("Young modulus (N/m2)")
        self.label_2.setText("Section area (m2)")
        self.label_3.setText("Section inertia (m4)")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Section")
        item = self.table.verticalHeaderItem(0)
        item.setText("1")
        item = self.table.horizontalHeaderItem(0)
        item.setText("member")
        item = self.table.horizontalHeaderItem(1)
        item.setText("load (N/m)")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), "Loads")
        item = self.table_2.verticalHeaderItem(0)
        item.setText("1")
        item = self.table_2.horizontalHeaderItem(0)
        item.setText("node")
        item = self.table_2.horizontalHeaderItem(1)
        item.setText("constraint")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), "Nodes")
        #addition
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.bGO.clicked.connect(results)

def results():
  # add section data and loads of the dialog
  E=float(ui.editE.text())
  I=float(ui.editI.text())
  A=float(ui.editA.text())
  ss=SystemElements()
  frame=FreeCAD.ActiveDocument.getObjectsByLabel(ui.comboBox.currentText())[0]
  sk=frame.Base
  for l in sk.Geometry:
    sp=[i*1e-3 for i in list(l.StartPoint)[:2]]
    ep=[i*1e-3 for i in list(l.EndPoint)[:2]]
    ss.add_element([sp,ep],EA=E*A,EI=E*I)
  for i in list(range(len(sk.Geometry))):
    if ui.table.item(i,1):
      item=ui.table.item(i,1)
      try:
        load=float(item.text())
        ss.q_load(element_id=(i+1), q=load)
      except:
        pass
  for i in list(range(ss.id_last_node)):
    if ui.table_2.item(i,1):
      if ui.table_2.item(i,1).text()=='fix':
        ss.add_support_fixed(node_id=i+1)
      elif ui.table_2.item(i,1).text()=='hinge':
        ss.add_support_hinged(node_id=i+1)
      elif ui.table_2.item(i,1).text()=='roll':
        ss.add_support_roll(node_id=i+1)
  ss.solve()
  ss.show_results()

def detectFrames():
  "detects framebranches in the doc and list their Base if it's a Sketch"
  for o in FreeCAD.ActiveDocument.Objects:
    if hasattr(o,'FType') and o.FType=='FrameBranch':
      if hasattr(o.Base,'TypeId') and o.Base.TypeId=='Sketcher::SketchObject':
        ui.comboBox.addItem(o.Label)

def redraw():
  frame=FreeCAD.ActiveDocument.getObjectsByLabel(ui.comboBox.currentText())[0]
  print(frame.Label)
  sk=frame.Base
  print('\tBase: '+sk.Label)
  A=frame.Profile.Shape.Area*1e-6
  I=frame.Profile.Shape.MatrixOfInertia.multiply(X).dot(X)*1e-12
  ss=SystemElements()
  for l in sk.Geometry:
    sp=[i*1e-3 for i in list(l.StartPoint)[:2]]
    ep=[i*1e-3 for i in list(l.EndPoint)[:2]]
    ss.add_element([sp,ep],EA=E*A,EI=E*I)
  print('\tNodes: %i\n\tElements: %i\n\n' %(ss.id_last_node, ss.id_last_element))
  ss.show_structure()
  ui.editE.setText(str(E))
  ui.editA.setText(str(A))
  ui.editI.setText(str(I))
  n=len(sk.Geometry)
  ui.table.setRowCount(n)
  for i in list(range(n)):
    item=QtGui.QTableWidgetItem('%.1f m' %(sk.Geometry[i].length()/1000))
    ui.table.setItem(i,0,item)
  ui. table.setItem(3,1,QtGui.QTableWidgetItem('-2000')) #for test
  ui. table.setItem(4,1,QtGui.QTableWidgetItem('-1000')) #for test
  ui.table_2.setRowCount(ss.id_last_node)
  for i in list(range(ss.id_last_node)):
    ui.table_2.setItem(i,0,QtGui.QTableWidgetItem('%.2f, %.2f' %ss.nodes_range('both')[i]))
  ui.table_2.setItem(0,1,QtGui.QTableWidgetItem('fix')) #for test
  ui.table_2.setItem(3,1,QtGui.QTableWidgetItem('roll')) #for test
  ui.table_2.setItem(5,1,QtGui.QTableWidgetItem('hinge')) #for test

# shows dialog to define loads and constraints
Dialog = QtGui.QDialog()
ui = Ui_Dialog()
ui.setupUi(Dialog)
detectFrames()
if ui.comboBox.currentText():
  redraw()
  Dialog.show()
else:
  FreeCAD.Console.PrintError("There must be a framebranch with a sketch base in active document.\n")
#frames=[t for t in FreeCAD.ActiveDocument.Objects if hasattr(t,'FType') and t.FType=='FrameBranch']
# if frames:
  # # creates a structure with the properties of the framebranch
  # sk=frames[0].Base
  # A=frames[0].Profile.Shape.Area*1e-6
  # I=frames[0].Profile.Shape.MatrixOfInertia.multiply(X).dot(X)*1e-12
  # ss=SystemElements()
  # for l in sk.Geometry:
    # sp=[i*1e-3 for i in list(l.StartPoint)[:2]]
    # ep=[i*1e-3 for i in list(l.EndPoint)[:2]]
    # ss.add_element([sp,ep],EA=E*A,EI=E*I)
  # ss.show_structure()
  # ui.editE.setText(str(E))
  # ui.editA.setText(str(A))
  # ui.editI.setText(str(I))
  # n=len(sk.Geometry)
  # ui.table.setRowCount(n)
  # for i in list(range(n)):
    # item=QtGui.QTableWidgetItem('%.1f m' %(sk.Geometry[i].length()/1000))
    # ui.table.setItem(i,0,item)
  # ui. table.setItem(3,1,QtGui.QTableWidgetItem('-2000')) #for test
  # ui. table.setItem(4,1,QtGui.QTableWidgetItem('-1000')) #for test
  # ui.table_2.setRowCount(ss.id_last_node)
  # for i in list(range(ss.id_last_node)):
    # ui.table_2.setItem(i,0,QtGui.QTableWidgetItem('%.2f, %.2f' %ss.nodes_range('both')[i]))
  # ui.table_2.setItem(0,1,QtGui.QTableWidgetItem('fix')) #for test
  # ui.table_2.setItem(3,1,QtGui.QTableWidgetItem('roll')) #for test
  # ui.table_2.setItem(5,1,QtGui.QTableWidgetItem('hinge')) #for test
  # Dialog.show()
