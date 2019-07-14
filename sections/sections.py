import FreeCAD, FreeCADGui, Part, Draft
from FreeCAD import Vector
from PySide.QtCore import *
from PySide.QtGui import *
from os.path import join, dirname, abspath

FTypes=['R','circle','T','H','L','U','Z','omega']

class protoTypeDialog(object): 
  'prototype for dialogs.ui with callback function'
  def __init__(self,dialog='anyFile.ui'):
    dialogPath=join(dirname(abspath(__file__)),"resources",dialog)
    self.form=FreeCADGui.PySideUic.loadUi(dialogPath)
    self.mw = FreeCADGui.getMainWindow()
    for act in self.mw.findChildren(QAction):
      if act.objectName() in ["actionX", "actionS"]:
        self.mw.removeAction(act)
    self.actionX = QAction(self.mw)
    self.actionX.setObjectName("actionX") # define X action
    self.actionX.setShortcut(QKeySequence("X"))
    self.actionX.triggered.connect(self.accept)
    self.mw.addAction(self.actionX)
    self.actionS = QAction(self.mw)
    self.actionS.setObjectName("actionS") # define S action
    self.actionS.setShortcut(QKeySequence("S"))
    self.actionS.triggered.connect(self.selectAction)
    self.mw.addAction(self.actionS)
    self.actionESC = QAction(self.mw)
    FreeCAD.Console.PrintMessage('"%s" to select; "%s" to execute\n' %(self.actionS.shortcuts()[0].toString(),self.actionX.shortcuts()[0].toString()))
    try:
      self.view=FreeCADGui.activeDocument().activeView()
      self.call=self.view.addEventCallback("SoMouseButtonEvent", self.action) # SoKeyboardEvents replaced by QAction'
    except:
      FreeCAD.Console.PrintError('No view available.\n')
  def action(self,arg):
    'Defines functions executed by the callback self.call when "SoMouseButtonEvent"'
    # SoKeyboardEvents replaced by QAction':
    CtrlAltShift=[arg['CtrlDown'],arg['AltDown'],arg['ShiftDown']]
    if arg['Button']=='BUTTON1' and arg['State']=='DOWN': self.mouseActionB1(CtrlAltShift)
    elif arg['Button']=='BUTTON2' and arg['State']=='DOWN': self.mouseActionB2(CtrlAltShift)
    elif arg['Button']=='BUTTON3' and arg['State']=='DOWN': self.mouseActionB3(CtrlAltShift)
  def selectAction(self):
    'MUST be redefined in the child class'
    print('"selectAction" performed')
    pass
  def mouseActionB1(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def mouseActionB2(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def mouseActionB3(self,CtrlAltShift):
    'MUST be redefined in the child class'
    pass
  def reject(self):
    'CAN be redefined to remove other attributes, such as arrow()s or label()s'
    self.mw.removeAction(self.actionX)
    self.mw.removeAction(self.actionS)
    FreeCAD.Console.PrintMessage('Actions "%s" and "%s" removed\n' %(self.actionX.objectName(),self.actionS.objectName()))
    try: self.view.removeEventCallback('SoMouseButtonEvent',self.call)
    except: pass
    FreeCADGui.Control.closeDialog()
    if FreeCAD.ActiveDocument: FreeCAD.ActiveDocument.recompute()

###### FUNCTIONS ##########

def doProfile(typeS="RH", label="Square", dims=[50,100,5]): # rearrange args in a better mnemonic way
  'doProfile(typeS, label, dims)'
  if typeS in["RH", "R", "H", "U", "L", "T", "Z", "omega","circle"]:
    profile=[0,'SECTION',label,typeS]+dims # for py2.6 versions
    obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython",profile[2])
    obj.Label = profile[2]
    if profile[3]=="RH":
        _ProfileRH(obj, profile)
    elif profile[3]=="R":
        _ProfileR(obj, profile)
    elif profile[3]=="U":
        _ProfileU(obj, profile)
    elif profile[3]=="T":
        _ProfileT(obj, profile)
    elif profile[3]=="H":
        _ProfileH(obj, profile)
    elif profile[3]=="L":
        _ProfileL(obj, profile)
    elif profile[3]=="Z":
        _ProfileZ(obj, profile)
    elif profile[3]=="omega":
        _ProfileOmega(obj, profile)
    elif profile[3]=="circle":
        _ProfileCircle(obj, profile)
    else :
        print("Profile not supported")
    if FreeCAD.GuiUp:
        Draft._ViewProviderDraft(obj.ViewObject)
    return obj
  else:
    FreeCAD.Console.PrintError('Not such section!\n')

def drawAndCenter (points):
    p = Part.makePolygon(points)
    s = Part.Face(p)
    v=s.CenterOfMass 
    points2 = [point.add(v.negative()) for point in points]
    p2 = Part.makePolygon(points2)
    return Part.Face(p2)

############ pointsXXX() functions #################

def pointsH(H, W, D, t1, t2, t3):
  p1 = Vector(0,0,0)
  p2 = Vector(W,0,0)
  p3 = Vector(W,t2,0) 
  p4 = Vector(W/2+t1/2,t2,0)
  p5 = Vector(W/2+t1/2,H-t3,0)
  p6 = Vector(W/2+D/2,H-t3,0)
  p7 = Vector(W/2+D/2,H,0)
  p8 = Vector(W/2-D/2,H,0)
  p9 = Vector(W/2-D/2,H-t3,0)
  p10 = Vector(W/2-t1/2,H-t3,0)
  p11 = Vector(W/2-t1/2,t2,0)
  p12 = Vector(0,t2,0)
  return [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1]

def pointsL(H,W,t1,t2):
  p1 = Vector(-W/2,-H/2,0)
  p2 = Vector(W/2,-H/2,0)
  p3 = Vector(W/2,H/2,0)
  p4 = Vector(W/2-t1,H/2,0)
  p5 = Vector(W/2-t1,t2-H/2,0)
  p6 = Vector(-W/2,t2-H/2,0)        
  return [p1,p2,p3,p4,p5,p6,p1]

def pointsOmega(H, W, D, t1, t2, t3):
  p1 = Vector(0,0,0)
  p2 = Vector(W,0,0)
  p3 = Vector(W,H-t3,0) 
  p4 = Vector(W+D-t1,H-t3,0)
  p5 = Vector(W+D-t1,H,0)
  p6 = Vector(W-t1,H,0)
  p7 = Vector(W-t1,t2,0)
  p8 = Vector(t1,t2,0)
  p9 = Vector(t1,H,0)
  p10 = Vector(t1-D,H,0)
  p11 = Vector(t1-D,H-t3,0)
  p12 = Vector(0,H-t3,0)
  return [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1]

def pointsT(H, W, t1, t2):
  p1 = Vector(-W/2,-H/2,0)
  p2 = Vector(W/2,-H/2,0)
  p3 = Vector(W/2,(-H/2)+t2,0)
  p4 = Vector(t1/2,(-H/2)+t2,0)
  p5 = Vector(t1/2,H/2,0)
  p6 = Vector(-t1/2,H/2,0)
  p7 = Vector(-t1/2,(-H/2)+t2,0)
  p8 = Vector(-W/2,(-H/2)+t2,0)
  return [p1,p2,p3,p4,p5,p6,p7,p8,p1]

def pointsU(H, W, D, t1, t2, t3):
  p1 = Vector(0,0,0)
  p2 = Vector(W,0,0)
  p3 = Vector(W,H,0) 
  p4 = Vector(W-D,H,0)
  p5 = Vector(W-D,H-t3,0)
  p6 = Vector(W-t1,H-t3,0)
  p7 = Vector(W-t1,t2,0)
  p8 = Vector(0,t2,0)
  return [p1,p2,p3,p4,p5,p6,p7,p8,p1]

def pointsZ(H,W,t1,t2):
  p1 = Vector(-t1/2,-W/2,0)
  p2 = Vector(-t1/2,(W/2)-t2,0)
  p3 = Vector(t1/2-H,(W/2)-t2,0)
  p4 = Vector(t1/2-H,W/2,0)
  p5 = Vector(t1/2,W/2,0)
  p6 = Vector(t1/2,t2-W/2,0)
  p7 = Vector(H-t1/2,t2-W/2,0)
  p8 = Vector(H-t1/2,-W/2,0)
  return [p1,p8,p7,p6,p5,p4,p3,p2,p1]

###### PROFILE EDITOR ########

# the icons 
pixs=[pixSquare,pixT,pixU,pixH,pixL,pixZ,pixOmega,pixCircle]=[QPixmap(join(dirname(abspath(__file__)),"resources",fileName)) for fileName in ["square.png","T.png","U.png","H.png","L.png","Z.png","omega.png","circle.png"]]

class profEdit(protoTypeDialog):
  def __init__(self):
    super(profEdit,self).__init__("sections.ui")
    self.setProfile('square')
    self.form.editB.editingFinished.connect(lambda: self.form.editD.setText(self.form.editB.text()))
    self.form.editT2.editingFinished.connect(lambda: self.form.editT3.setText(self.form.editT2.text()))
    self.form.tbSquare.clicked.connect(lambda: self.setProfile('square'))
    self.form.tbCircle.clicked.connect(lambda: self.setProfile('circle'))
    self.form.tbT.clicked.connect(lambda: self.setProfile('T'))
    self.form.tbU.clicked.connect(lambda: self.setProfile('U'))
    self.form.tbH.clicked.connect(lambda: self.setProfile('H'))
    self.form.tbL.clicked.connect(lambda: self.setProfile('L'))
    self.form.tbZ.clicked.connect(lambda: self.setProfile('Z'))
    self.form.btn1.clicked.connect(self.apply)
    self.form.btn2.clicked.connect(lambda: self.shiftProfile(None))
    self.form.tbOmega.clicked.connect(lambda: self.setProfile('omega'))
    for z in list(zip(pixs,[self.form.tbSquare,self.form.tbT,self.form.tbU,self.form.tbH,self.form.tbL,self.form.tbZ,self.form.tbOmega,self.form.tbCircle])):
      icon = QIcon()
      icon.addPixmap(z[0], QIcon.Normal, QIcon.Off)
      z[1].setIcon(icon)
  def setProfile(self, typeS):
    if typeS=='square':
      self.form.labImg.setPixmap(pixSquare)
      self.type="R"
      self.label="Square"
    elif typeS=='T':
      self.form.labImg.setPixmap(pixT)
      self.type="T"
      self.label="T-profile"
    elif typeS=='U':
      self.form.labImg.setPixmap(pixU)
      self.type="U"
      self.label="U-profile"
    elif typeS=='H':
      self.form.labImg.setPixmap(pixH)
      self.type="H"
      self.label="H-profile"
    elif typeS=='L':
      self.form.labImg.setPixmap(pixL)
      self.type="L"
      self.label="L-profile"
    elif typeS=='Z':
      self.form.labImg.setPixmap(pixZ)
      self.type="Z"
      self.label="Z-profile"
    elif typeS=='omega':
      self.form.labImg.setPixmap(pixOmega)
      self.type="omega"
      self.label="Omega-profile"
    elif typeS=='circle':
      self.form.labImg.setPixmap(pixCircle)
      self.type="circle"
      self.label="Circle-profile"
  def accept(self):
    D, H, B, t1, t2, t3 = float(self.form.editD.text()),\
                          float(self.form.editH.text()),\
                          float(self.form.editB.text()),\
                          float(self.form.editT1.text()),\
                          float(self.form.editT2.text()),\
                          float(self.form.editT3.text())
    if not self.form.lineEdit.text(): label=self.label
    else: label= self.form.lineEdit.text()
    if FreeCAD.ActiveDocument:
      FreeCAD.activeDocument().openTransaction('Insert profile')
      if self.type=='R':
        if not self.form.cbFull.isChecked() and t2<H/2 and t1<B/2:
          sect=doProfile("RH",label,[B,H,t1,t2])
        else:
          sect=doProfile("R",label,[B,H])
      elif self.type=='H':
        sect=doProfile(self.type,label,[B,H,D,t1,t2,t3])
      elif self.type=='U' and t2<H and t1<B/2:
        sect=doProfile(self.type,label,[B,H,D,t1,t2,t3])
      elif self.type=='L' and t2<H and t1<B:
        sect=doProfile(self.type,label,[B,H,t1,t2])
      elif self.type=='T' and t2<H and t1<B:
        sect=doProfile(self.type,label,[B,H,t1,t2])
      elif self.type=='Z'and t2<H/2 and t1<B*2:
        sect=doProfile(self.type,label,[B,H,t1,t2])
      elif self.type=='omega':
        sect=doProfile(self.type,label,[B,H,D,t1,t2,t3])
      elif self.type=='circle':
        if self.form.cbFull.isChecked():
          sect=doProfile(self.type,label,[D,0])
        else:
          sect=doProfile(self.type,label,[D,t1])
      FreeCAD.ActiveDocument.recompute()
      self.shiftProfile(sect)
      FreeCAD.activeDocument().commitTransaction()
      FreeCAD.ActiveDocument.recompute()
      FreeCAD.ActiveDocument.recompute()
  def apply(self):
    D, H, B, t1, t2, t3 = float(self.form.editD.text()),\
                          float(self.form.editH.text()),\
                          float(self.form.editB.text()),\
                          float(self.form.editT1.text()),\
                          float(self.form.editT2.text()),\
                          float(self.form.editT3.text())
    sel=FreeCADGui.Selection.getSelection()
    if sel:
      obj=sel[0]
      if hasattr(obj,'Shape') and obj.Shape.ShapeType in ('Face','Shell'):
        if hasattr(obj,'H'):
          obj.H=H
        if hasattr(obj,'W'):
          obj.W=B
        if hasattr(obj,'D'):
          obj.D=D
        if hasattr(obj,'t1'):
          obj.t1=t1
        if hasattr(obj,'t2'):
          obj.t2=t2
        if hasattr(obj,'t3'):
          obj.t3=t3
      FreeCAD.ActiveDocument.recompute()
  def mouseActionB1(self,CtrlAltShift):
    v = FreeCADGui.ActiveDocument.ActiveView
    i = v.getObjectInfo(v.getCursorPos())
    if i: 
      labText=i['Object']
      obj=FreeCAD.ActiveDocument.getObject(i['Object'])
      if hasattr(obj,'FType') and obj.FType in FTypes:
        if obj.FType=='R':
          self.setProfile('R')
        elif obj.FType=='circle':
          self.setProfile('circle')
        elif obj.FType=='T':
          self.setProfile('T')
        elif obj.FType=='H':
          self.setProfile('H')
        elif obj.FType=='L':
          self.setProfile('L')
        elif obj.FType=='U':
          self.setProfile('U')
        elif obj.FType=='Z':
          self.setProfile('Z')
        elif obj.FType=='omega':
          self.setProfile('omega')
        ###############
        self.form.lineEdit.setText(obj.Label)
        if hasattr(obj,'H'): self.form.editH.setText(str(float(obj.H.Value)))
        else: self.form.editH.setText('0')
        if hasattr(obj,'W'): self.form.editB.setText(str(float(obj.W)))
        else: self.form.editW.setText('0')
        if hasattr(obj,'D'): self.form.editD.setText(str(float(obj.D)))
        else: self.form.editD.setText('0')
        if hasattr(obj,'t1'): self.form.editT1.setText(str(float(obj.t1)))
        else: self.form.editT1.setText('0')
        if hasattr(obj,'t2'): self.form.editT2.setText(str(float(obj.t2)))
        else: self.form.editT2.setText('0')
        if hasattr(obj,'t3'): self.form.editT3.setText(str(float(obj.t3)))
        else: self.form.editT3.setText('0')
        # self.form.labSelect.setText(obj.Label)
    else:
      self.form.editH.setText('80')
      self.form.editB.setText('45')
      self.form.editD.setText('45')
      self.form.editT1.setText('5')
      self.form.editT2.setText('5')
      self.form.editT3.setText('5')
      self.form.lineEdit.setText('')
  def shiftProfile (self,sect=None):
    if not sect:
      sel=FreeCADGui.Selection.getSelection()
      if sel and hasattr(sel[0],'FType'): sect=sel[0]
    if sect:
      sect.Placement.move(sect.Shape.CenterOfMass.negative())
      FreeCAD.ActiveDocument.recompute()
      FreeCAD.ActiveDocument.openTransaction('Shift profile')
      B=sect.Shape.BoundBox
      O=sect.Shape.CenterOfMass
      N=FreeCAD.Vector(0,O.y-B.YMin,0)
      S=FreeCAD.Vector(0,O.y-B.YMax,0)
      E=FreeCAD.Vector(O.x-B.XMin,0,0)
      W=FreeCAD.Vector(O.x-B.XMax,0,0)
      delta=FreeCAD.Vector() 
      if self.form.rbN.isChecked(): 
        delta=S
      elif self.form.rbS.isChecked(): 
        delta=N
      elif self.form.rbE.isChecked(): 
        delta=W
      elif self.form.rbW.isChecked(): 
        delta=E
      elif self.form.rbNE.isChecked(): 
        delta=S.add(W)
      elif self.form.rbNW.isChecked(): 
        delta=S.add(E)
      elif self.form.rbSE.isChecked(): 
        delta=N.add(W)
      elif self.form.rbSW.isChecked(): 
        delta=N.add(E)
      elif self.form.rbC.isChecked():
        delta=O*-1
      sect.Placement.move(delta)
      FreeCAD.ActiveDocument.commitTransaction()

########### _ ProfileXXX() classes ###############

from ArchProfile import _Profile

class _ProfileRH(_Profile):
    '''A parametric Rectangular hollow beam profile. Profile data: [width, height, thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'RH'
        obj.addProperty("App::PropertyLength","W","Draft","Width of the beam").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[5]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness of the vertical sides").t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness of the horizontal sides").t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        p1 = Vector(-W/2,-H/2,0)
        p2 = Vector(W/2,-H/2,0)
        p3 = Vector(W/2,H/2,0)
        p4 = Vector(-W/2,H/2,0)
        q1 = Vector(-W/2+t1,-H/2+t2,0)
        q2 = Vector(W/2-t1,-H/2+t2,0)
        q3 = Vector(W/2-t1,H/2-t2,0)
        q4 = Vector(-W/2+t1,H/2-t2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p1])
        q = Part.makePolygon([q1,q2,q3,q4,q1])
        obj.Shape = Part.Face(p).cut(Part.Face(q))
        
class _ProfileR(_Profile):
    '''A parametric Rectangular solid beam profile. Profile data: [width, height]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'R'
        obj.addProperty("App::PropertyLength","W","Draft","Width of the beam").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[5]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H= obj.W.Value, obj.H.Value
        p1 = Vector(-W/2,-H/2,0)
        p2 = Vector(W/2,-H/2,0)
        p3 = Vector(W/2,H/2,0)
        p4 = Vector(-W/2,H/2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p1])
        obj.Shape = Part.Face(p)

class _ProfileCircle(_Profile):
    '''A parametric circular beam profile. 
    Profile data: 
      D: diameter
      t1: thickness (optional; "0" for solid section)'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'circle'
        obj.addProperty("App::PropertyLength","D","Draft","Diameter of the beam").D = profile[4]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness").t1 = profile[5]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        D,t1= obj.D.Value, obj.t1.Value
        if not t1:
          obj.Shape = Part.makeFace([Part.makeCircle(D/2)],"Part::FaceMakerSimple")
        elif t1<D/2:
          c1=Part.makeFace([Part.makeCircle(D/2)],"Part::FaceMakerSimple")
          c2=Part.makeFace([Part.makeCircle(D/2-t1)],"Part::FaceMakerSimple")
          obj.Shape = c1.cut(c2)  
        
class _ProfileL(_Profile):
    '''A parametric L beam profile. Profile data: [width, height, web thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'L'
        obj.addProperty("App::PropertyLength","W","Draft","W of the beam").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[5]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness of the webs").t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness of the webs").t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        obj.Shape = drawAndCenter(pointsL(H,W,t1,t2))

class _ProfileT(_Profile):
    '''A parametric T beam profile. Profile data: [width, height, web thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'T'
        obj.addProperty("App::PropertyLength","W","Draft","W of the beam").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","H of the beam").H = profile[5]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness of the web").t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness of the web").t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        obj.Shape = drawAndCenter(pointsT(H,W,t1,t2))

class _ProfileZ(_Profile):
    '''A parametric Z beam profile. Profile data: [width, height, web thickness, flange thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'Z'
        obj.addProperty("App::PropertyLength","W","Draft","Width of the beam").W = profile[5]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[4]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness of the web").t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness of the flanges").t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        obj.Shape = drawAndCenter(pointsZ(H,W,t1,t2))

class _ProfileOmega(_Profile):
    '''A parametric omega beam profile. Profile data: [W, H, D, t1,t2,t3]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'omega'
        obj.addProperty("App::PropertyLength","W","Draft","Width of the beam").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[5]
        obj.addProperty("App::PropertyLength","D","Draft","Width of the flanges").D = profile[6]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness 1").t1 = profile[7]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness 2").t2 = profile[8]
        obj.addProperty("App::PropertyLength","t3","Draft","Thickness 3").t3 = profile[9]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, D, t1, t2, t3 = obj.W.Value, obj.H.Value, obj.D.Value, obj.t1.Value, obj.t2.Value,obj.t3.Value, 
        obj.Shape = drawAndCenter(pointsOmega(H,W,D,t1,t2,t3))

class _ProfileH(_Profile):
    '''A parametric omega beam profile. Profile data: [W, H, D, t1,t2,t3]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'H'
        obj.addProperty("App::PropertyLength","W","Draft","Width of the bottom flange").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[5]
        obj.addProperty("App::PropertyLength","D","Draft","Width of the top flange").D = profile[6]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness 1").t1 = profile[7]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness 2").t2 = profile[8]
        obj.addProperty("App::PropertyLength","t3","Draft","Thickness 3").t3 = profile[9]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, D, t1, t2, t3 = obj.W.Value, obj.H.Value, obj.D.Value, obj.t1.Value, obj.t2.Value,obj.t3.Value, 
        obj.Shape = drawAndCenter(pointsH(H,W,D,t1,t2,t3))

class _ProfileU(_Profile):
    '''A parametric U beam profile. Profile data: [W, H, D, t1,t2,t3]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyString","FType","Profile","Type of section").FType = 'U'
        obj.addProperty("App::PropertyLength","W","Draft","Width of the bottom flange").W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft","Height of the beam").H = profile[5]
        obj.addProperty("App::PropertyLength","D","Draft","Width of the top flange").D = profile[6]
        obj.addProperty("App::PropertyLength","t1","Draft","Thickness 1").t1 = profile[7]
        obj.addProperty("App::PropertyLength","t2","Draft","Thickness 2").t2 = profile[8]
        obj.addProperty("App::PropertyLength","t3","Draft","Thickness 3").t3 = profile[9]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        W, H, D, t1, t2, t3 = obj.W.Value, obj.H.Value, obj.D.Value, obj.t1.Value, obj.t2.Value,obj.t3.Value, 
        obj.Shape = drawAndCenter(pointsU(H,W,D,t1,t2,t3))

FreeCADGui.Control.showDialog(profEdit())
