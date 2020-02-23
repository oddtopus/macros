# copyright 2020
# licence LGPL3 (https://github.com/oddtopus/macros/LICENSE)

from PySide import QtCore, QtGui

class moverDialog(QtGui.QDialog):
    def __init__(self):
        super(moverDialog,self).__init__()
        self.resize(400, 250)
        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.labPos = QtGui.QLabel(self)
        self.labPos.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labPos)
        self.labObj = QtGui.QLabel(self)
        self.labObj.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.labObj)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label_2)
        self.frame = QtGui.QFrame(self)
        self.frame.setMinimumSize(QtCore.QSize(0, 50))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.rbCenter = QtGui.QRadioButton(self.frame)
        self.rbCenter.setChecked(True)
        self.gridLayout.addWidget(self.rbCenter, 0, 1, 1, 1)
        self.rbNearest = QtGui.QRadioButton(self.frame)
        self.gridLayout.addWidget(self.rbNearest, 1, 1, 1, 1)
        self.rbNone = QtGui.QRadioButton(self.frame)
        self.gridLayout.addWidget(self.rbNone, 0, 0, 2, 1)
        self.verticalLayout.addWidget(self.frame)
        self.label = QtGui.QLabel(self)
        self.label.setMinimumSize(QtCore.QSize(0, 50))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.setWindowTitle("mover")
        self.labPos.setText("<pos>")
        self.labObj.setText("<obj>")
        self.label_2.setText("Anchors:")
        self.rbCenter.setText("center")
        self.rbNearest.setText("nearest")
        self.rbNone.setText("none")
        self.label.setText("left-click to grab or drop object\n"
"Ctrl + move to hold the object")

import FreeCAD, FreeCADGui
from os.path import join, dirname, abspath

class mover(object): 
  'prototype for dialogs.ui with callback function'
  def __init__(self):
    #dialogPath=join(dirname(abspath(__file__)),'moverDialog.ui')
    self.form=moverDialog() #FreeCADGui.PySideUic.loadUi(dialogPath)
    self.obj=None
    self.release=False
    try:
      self.view=FreeCADGui.activeDocument().activeView()
      self.call=self.view.addEventCallback("SoMouseButtonEvent", self.action) # SoKeyboardEvents replaced by QAction'
    except:
      FreeCAD.Console.PrintError('No view available.\n')
  def action(self,arg):
    'Defines functions executed by the callback self.call when "SoMouseButtonEvent"'
    CtrlAltShift=[arg['CtrlDown'],arg['AltDown'],arg['ShiftDown']]
    if arg['Button']=='BUTTON1' and arg['State']=='DOWN': self.mouseActionB1(CtrlAltShift)
    elif arg['Button']=='BUTTON2' and arg['State']=='DOWN': self.mouseActionB2(CtrlAltShift)
    elif arg['Button']=='BUTTON3' and arg['State']=='DOWN': self.mouseActionB3(CtrlAltShift)
  def mouseActionB1(self,CtrlAltShift):
    v = FreeCADGui.ActiveDocument.ActiveView
    FreeCADGui.Selection.clearPreselection()
    if self.release:#CtrlAltShift[0]:
      self.obj=None
      self.release=False
      self.form.labObj.setText('---')
      try: 
        self.view.removeEventCallback("SoLocation2Event",self.callbackMove)
        self.callbackMove=None
      except: 
        pass
    else:
      infos = v.getObjectInfo(v.getCursorPos())
      if infos and not self.obj:
        FreeCAD.Console.PrintMessage('pos=%i,%i,%i\nobj=%s/%s' %(infos['x'],infos['y'],infos['z'],infos['Object'],infos['Component']))
        self.obj=FreeCAD.ActiveDocument.getObject(infos['Object'])
        self.form.labObj.setText(self.obj.Label)
        self.callbackMove = self.view.addEventCallback("SoLocation2Event",self.moveMouse)
        self.release=True
  def mouseActionB2(self,CtrlAltShift):
    pass
  def mouseActionB3(self,CtrlAltShift):
    pass
  def moveMouse(self, info):
    point=self.view.getPoint( *info['Position'] )
    self.form.labPos.setText('%.1f ,%.1f, %.1f' %tuple(point))
    ps=FreeCADGui.Selection.getPreselection()
    n1=self.obj.Placement.Rotation.multVec(FreeCAD.Vector(0.0,0.0,1.0)).normalize()
    n2=False
    pos=self.obj.Placement.Base
    if not info['CtrlDown']:
      if not self.form.rbNone.isChecked(): # anchor != none
        if ps.ObjectName and ps.ObjectName!=self.obj.Name: 
          if ps.SubElementNames[0][:6]=='Vertex': # vertex <=> move to point
            self.obj.Placement.Base = ps.SubObjects[0].Point
          elif ps.SubElementNames[0][:4]=='Face':  # face <=> move to surface and align to normal
            if self.form.rbNearest.isChecked():
              self.obj.Placement.Base = ps.PickedPoints[0] 
            elif self.form.rbCenter.isChecked():
              self.obj.Placement.Base = ps.SubObjects[0].CenterOfMass
            n2=ps.SubObjects[0].normalAt(0,0) # orientation = normal
            rot=FreeCAD.Rotation(n1,n2)
            self.obj.Placement.Rotation=rot.multiply(self.obj.Placement.Rotation)
          elif ps.SubElementNames[0][:4]=='Edge': # edge <=> ..
            if self.form.rbNearest.isChecked():
              self.obj.Placement.Base = ps.PickedPoints[0]
              n2=ps.SubObjects[0].tangentAt(0)
            elif self.form.rbCenter.isChecked():
              if not ps.SubObjects[0].curvatureAt(0): # edge is straight
                if hasattr(self.obj,'Height'):
                  self.obj.Placement.Base = ps.SubObjects[0].CenterOfMass-n1.multiply(self.obj.Height/2)
                else:
                  self.obj.Placement.Base = ps.SubObjects[0].valueAt(0)+ps.SubObjects[0].tangentAt(0).multiply(float(ps.SubObjects[0].Length)/2)
                n2=ps.SubObjects[0].tangentAt(0)
              else:                                   # edge is curved
                self.obj.Placement.Base = ps.SubObjects[0].centerOfCurvatureAt(0)
                n2=ps.SubObjects[0].tangentAt(0).cross(ps.SubObjects[0].normalAt(0))
            if n2: 
              self.obj.Placement.Rotation=FreeCAD.Rotation(FreeCAD.Vector(0,0,1),n2)
      else: #anchor==none
        self.obj.Placement.Base = point
  def accept(self):
    pass
  def reject(self):
    'CAN be redefined to remove other attributes, such as arrow()s or label()s'
    try: self.view.removeEventCallback('SoMouseButtonEvent',self.call)
    except: pass
    try: self.view.removeEventCallback("SoLocation2Event",self.callbackMove)
    except:pass
    FreeCADGui.Control.closeDialog()
    if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()


FreeCADGui.Control.showDialog(mover())
