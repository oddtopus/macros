#****************************************************************************
#*                                                                          *
#*   An anastruct's frontend for FreeCAD                                    *
#*   Requires libraries dodo, anastruct and a release of FC with Py3/Qt5    *
#*   Copyright (c) 2019 Riccardo Treu LGPL                                  *
#*                                                                          *
#*   For anastruct, Copyright 2018, Ritchie Vink                            *
#*   https://github.com/ritchie46                                           *
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
E=2.1e11 # N/m2 --- steel
X=FreeCAD.Vector(1,0,0)
from PySide.QtCore import *
from PySide.QtGui import *
from sys import platform
from os.path import join, dirname, abspath
import FreeCAD, FreeCADGui

def detectFrames():
  "detects framebranches in the doc and list their Base if it's a Sketch"
  validFrames=list()
  for o in FreeCAD.ActiveDocument.Objects:
    if hasattr(o,'FType') and o.FType=='FrameBranch':
      if hasattr(o.Base,'TypeId') and o.Base.TypeId=='Sketcher::SketchObject':
        validFrames.append(o.Label)
  return validFrames

import dodoDialogs
from uCmd import label3D

class astructDialog(dodoDialogs.protoTypeDialog): #(object):
  'prototype for dialogs.ui with callback function'
  def __init__(self):
    dialogPath=join(dirname(abspath(__file__)),"anastruct6.ui") 
    super(astructDialog,self).__init__("anastruct6.ui")
    self.form.comboBox.addItems(detectFrames())
    self.form.comboBox.currentIndexChanged['int'].connect(self.redraw)
    self.labNodes=list()
    self.labEl=list()
    self.combos=list()
    self.combotypes=list()
    self.form.radioTruss.clicked.connect(self.setCalc)
    self.form.radioFrame.clicked.connect(self.setCalc)
    self.form.btnTruss.clicked.connect(lambda: self.setAll(1))
    self.form.btnFrame.clicked.connect(lambda: self.setAll(0))
    if self.form.comboBox.currentText():
      self.redraw()
  def setAll(self, index):
    for c in self.combotypes: c.setCurrentIndex(index)
  def setCalc(self):
    if self.form.radioTruss.isChecked():
      for c in self.combotypes: 
        c.setCurrentIndex(1)
        c.setEnabled(False)
        self.form.btnFrame.setEnabled(False)
        self.form.btnTruss.setEnabled(False)
    else:
      for c in self.combotypes: 
        c.setCurrentIndex(0)
        c.setEnabled(True)
        self.form.btnFrame.setEnabled(True)
        self.form.btnTruss.setEnabled(True)
  def accept(self):
    try:
      E=float(self.form.editE.text())
      I=float(self.form.editI.text())
      A=float(self.form.editA.text())
      ss=SystemElements()
      frame=FreeCAD.ActiveDocument.getObjectsByLabel(self.form.comboBox.currentText())[0]
      sk=frame.Base
      j=0
      print(self.combotypes)
      # CREATE MEMBERS OF STRUCTURE
      for l in sk.Geometry:
        sp=[i*1e-3 for i in list(l.StartPoint)[:2]]
        ep=[i*1e-3 for i in list(l.EndPoint)[:2]]
        if self.combotypes[j].currentText()=='beam': 
          ss.add_element([sp,ep],EA=E*A,EI=E*I)
        elif self.combotypes[j].currentText()=='truss': 
          ss.add_truss_element([sp,ep],EA=E*A)
        j+=1
      # SET DISTRIBUTED LOADS
      if self.form.radioFrame.isChecked():
        for i in list(range(len(sk.Geometry))):
          if self.form.tableDistrib.item(i,2):
            item=self.form.tableDistrib.item(i,2)
            try:
              load=float(item.text())
              ss.q_load(element_id=(i+1), q=load)
            except:
              pass
      for c in self.combos:
        i=self.combos.index(c)+1
        # SET NODE CONSTRAINTS
        if c.currentText()=='fix': ss.add_support_fixed(node_id=i)
        elif c.currentText()=='hinge': ss.add_support_hinged(node_id=i)
        elif c.currentText()=='roll': ss.add_support_roll(node_id=i)
        # SET NODE FORCES
        if self.form.tableConc.item(i-1,1) or self.form.tableConc.item(i-1,2):
          itemX=self.form.tableConc.item(i-1,1)
          try:    loadX=float(itemX.text())
          except: loadX=0
          itemY=self.form.tableConc.item(i-1,2)
          try:    loadY=float(itemY.text())
          except: loadY=0
          ss.point_load(node_id=(i), Fx=loadX, Fy=loadY)
      # SOLVE AND VALIDATE
      ss.solve()
      # stable=ss.validate(.0000001)
      # SHOW RESULTS ACCORDING THE CALC TYPE
      if True:#stable:
        if self.form.radioFrame.isChecked():
          ss.show_results()
        elif self.form.radioTruss.isChecked():
          ss.show_axial_force()
      else:
        FreeCAD.Console.PrintError('The structure is not stable.\n')
    except:
      FreeCAD.Console.PrintError('Invalid input\n')
      for l in self.labNodes+self.labEl:
        l. removeLabel()
  def reject(self):
    for l in self.labNodes+self.labEl:
      l.removeLabel()
    super(astructDialog,self).reject()
  def redraw(self):
    for l in self.labNodes+self.labEl:
      l.removeLabel()
    if self.form.comboBox.currentText():
      frame=FreeCAD.ActiveDocument.getObjectsByLabel(self.form.comboBox.currentText())[0]
      sk=frame.Base
      A=frame.Profile.Shape.Area*1e-6
      I=frame.Profile.Shape.MatrixOfInertia.multiply(X).dot(X)*1e-12
      ss=SystemElements()
      i=1
      for l in sk.Geometry:
        sp=[i*1e-3 for i in list(l.StartPoint)[:2]]
        ep=[i*1e-3 for i in list(l.EndPoint)[:2]]
        ss.add_element([sp,ep],EA=E*A,EI=E*I)
        p2=FreeCAD.Placement()
        p2.Base=sk.Placement.multVec((l.StartPoint+l.EndPoint)/2)
        self.labNodes.append(label3D(pl=p2, color=(0,0.8,0), text='____beam'+str(i)))
        i+=1
      nodes=ss.nodes_range('both')
      coords=[FreeCAD.Vector(n[0]*1000,n[1]*1000,0) for n in nodes]
      globalCoords=[sk.Placement.multVec(c) for c in coords]
      i=1
      for gc in globalCoords:
        self.labNodes.append(label3D(pl=FreeCAD.Placement(gc,FreeCAD.Rotation()), text='____node'+str(i)))
        i+=1
      self.form.editE.setText(str(E))
      self.form.editA.setText(str(A))
      self.form.editI.setText(str(I))
      n=len(sk.Geometry)
      self.form.tableDistrib.setRowCount(n)
      self.combotypes.clear()
      for i in list(range(n)):
        item=QTableWidgetItem('%.1f m' %(sk.Geometry[i].length()/1000))
        self.form.tableDistrib.setItem(i,0,item)
        self.combotypes.append(QComboBox())
        self.combotypes[-1].addItems(['beam','truss'])
        self.form.tableDistrib.setCellWidget(i,1,self.combotypes[-1])
      #self.form. tableDistrib.setItem(0,1,QTableWidgetItem('1000')) #for test
      self.form.table_2.setRowCount(ss.id_last_node)
      self.form.tableConc.setRowCount(ss.id_last_node)
      self.combos.clear()
      for i in list(range(ss.id_last_node)):
        self.form.table_2.setItem(i,0,QTableWidgetItem('%.2f, %.2f' %ss.nodes_range('both')[i]))
        self.combos.append(QComboBox())
        self.combos[-1].addItems(['-','fix','hinge','roll'])
        self.form.table_2.setCellWidget(i,1,self.combos[-1])
        self.form.tableConc.setItem(i,0,QTableWidgetItem('%.2f, %.2f' %ss.nodes_range('both')[i]))

FreeCADGui.Control.showDialog(astructDialog())
