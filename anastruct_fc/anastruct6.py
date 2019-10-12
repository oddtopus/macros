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
    #self.form=FreeCADGui.PySideUic.loadUi(dialogPath)
    self.form.comboBox.addItems(detectFrames())
    #self.form.bGO.clicked.connect(self.results)
    self.form.comboBox.currentIndexChanged['int'].connect(self.redraw)
    self.labNodes=list()
    self.labEl=list()
    if self.form.comboBox.currentText():
      self.redraw()
  def accept(self):
    try:
      E=float(self.form.editE.text())
      I=float(self.form.editI.text())
      A=float(self.form.editA.text())
      ss=SystemElements()
      frame=FreeCAD.ActiveDocument.getObjectsByLabel(self.form.comboBox.currentText())[0]
      sk=frame.Base
      for l in sk.Geometry:
        sp=[i*1e-3 for i in list(l.StartPoint)[:2]]
        ep=[i*1e-3 for i in list(l.EndPoint)[:2]]
        if self.form.radioFrame.isChecked():
          ss.add_element([sp,ep],EA=E*A,EI=E*I)
        elif self.form.radioTruss.isChecked():
          ss.add_truss_element([sp,ep],EA=E*A)
      for i in list(range(len(sk.Geometry))):
        if self.form.tableDistrib.item(i,1):
          item=self.form.tableDistrib.item(i,1)
          try:
            load=float(item.text())
            ss.q_load(element_id=(i+1), q=load)
          except:
            pass
      for i in list(range(ss.id_last_node)):
        if self.form.table_2.item(i,1):
          if self.form.table_2.item(i,1).text()=='fix':
            ss.add_support_fixed(node_id=i+1)
          elif self.form.table_2.item(i,1).text()=='hinge':
            ss.add_support_hinged(node_id=i+1)
          elif self.form.table_2.item(i,1).text()=='roll':
            ss.add_support_roll(node_id=i+1)
        if self.form.tableConc.item(i,1) or self.form.tableConc.item(i,2):
          itemX=self.form.tableConc.item(i,1)
          itemY=self.form.tableConc.item(i,2)
          try:    loadX=float(itemX.text())
          except: loadX=0
          try:    loadY=float(itemY.text())
          except: loadY=0
          ss.point_load(node_id=(i+1), Fx=loadX, Fy=loadY)
      ss.solve()
      if self.form.radioFrame.isChecked():
        ss.show_results()
      elif self.form.radioTruss.isChecked():
        ss.show_axial_force()
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
        p1=FreeCAD.Placement()
        p1.Base=sk.Placement.multVec(l.StartPoint)
        self.labNodes.append(label3D(pl=p1, text='____node'+str(i)))
        p2=FreeCAD.Placement()
        p2.Base=sk.Placement.multVec((l.StartPoint+l.EndPoint)/2)
        self.labNodes.append(label3D(pl=p2, color=(0,0.8,0), text='____beam'+str(i)))
        i+=1
      p1=FreeCAD.Placement()
      p1.Base=sk.Placement.multVec(l.EndPoint)
      self.labNodes.append(label3D(pl=p1, text='____node'+str(i)))
      l=sk.Geometry[-1]
      #ss.show_structure()
      nodes=ss.nodes_range('both')
      coords=[FreeCAD.Vector(n[0]*1000,n[1]*1000,0) for n in nodes]
      i=1
      # for c in coords:
        # print('Node %i: %.2f,%.2f,%.2f' %tuple([i]+list(c)))
        # i+=1
      self.form.editE.setText(str(E))
      self.form.editA.setText(str(A))
      self.form.editI.setText(str(I))
      n=len(sk.Geometry)
      self.form.tableDistrib.setRowCount(n)
      for i in list(range(n)):
        item=QTableWidgetItem('%.1f m' %(sk.Geometry[i].length()/1000))
        self.form.tableDistrib.setItem(i,0,item)
      self.form. tableDistrib.setItem(0,1,QTableWidgetItem('1000')) #for test
      self.form.table_2.setRowCount(ss.id_last_node)
      self.form.tableConc.setRowCount(ss.id_last_node)
      for i in list(range(ss.id_last_node)):
        self.form.table_2.setItem(i,0,QTableWidgetItem('%.2f, %.2f' %ss.nodes_range('both')[i]))
        self.form.tableConc.setItem(i,0,QTableWidgetItem('%.2f, %.2f' %ss.nodes_range('both')[i]))
      self.form.table_2.setItem(0,1,QTableWidgetItem('fix')) #for test

FreeCADGui.Control.showDialog(astructDialog())
