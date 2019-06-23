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

# based on ArchProfile.py by Yorik Van Havre () and additions by Renato Rivo ()

import FreeCAD, Draft, os, ArchProfile
from FreeCAD import Vector
import csv
if FreeCAD.GuiUp:
    import FreeCADGui
    from PySide import QtCore, QtGui
    from DraftTools import translate
    from PySide.QtCore import QT_TRANSLATE_NOOP
else:
    # \cond
    def translate(ctxt,txt):
        return txt
    def QT_TRANSLATE_NOOP(ctxt,txt):
        return txt
    # \endcond

def doProfile(typeS="RH", label="Square", dims=[50,100,5]): # rearrange args in a better mnemonic way
  'doProfile(typeS, label, dims)'
  if typeS in["RH", "R", "H", "U", "L", "T", "Z", "CC"]:
    argv=[0,'SECTION',label,typeS]+dims # for py2.6 versions
    return makeProfile(argv)#[0,'SECTION',label,typeS,*dims])
  else:
    FreeCAD.Console.PrintError('Not such section!\n')

def makeProfile(profile=[0,'REC','REC100x100','R',100,100]):
    '''makeProfile(profile): returns a shape  with the face defined by the profile data'''
    obj = FreeCAD.ActiveDocument.addObject("Part::Part2DObjectPython",profile[2])
    obj.Label = translate("Arch",profile[2])
    if profile[3]=="RH":
        _ProfileRH(obj, profile)
    elif profile[3]=="R":
        ArchProfile._ProfileR(obj, profile)
    elif profile[3]=="U":
        ArchProfile._ProfileU(obj, profile)
    elif profile[3]=="T":
        _ProfileT(obj, profile)
    # elif profile[3]=="H":                 #TODO
        # _ProfileH(obj, profile)
    elif profile[3]=="L":
        _ProfileL(obj, profile)
    elif profile[3]=="Z":
        _ProfileZ(obj, profile)
    # elif profile[3]=="CC":                 #TODO
        # _ProfileCC(obj, profile)
    else :
        print("Profile not supported")
    if FreeCAD.GuiUp:
        Draft._ViewProviderDraft(obj.ViewObject)
    return obj

class _Profile(Draft._DraftObject):
    '''Superclass for Profile classes'''

    def __init__(self,obj, profile):
        self.Profile=profile
        Draft._DraftObject.__init__(self,obj,"Profile")

class _ProfileRH(_Profile):
    '''A parametric Rectangular hollow beam profile. Profile data: [width, height, thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","W","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).H = profile[5]
        obj.addProperty("App::PropertyLength","t1","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the vertical sides")).t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the horizontal sides")).t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        import Part
        pl = obj.Placement
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
        #r.reverse()
        obj.Shape = Part.Face(p).cut(Part.Face(q))
        obj.Placement = pl
        
class _ProfileL(_Profile):
    '''A parametric L beam profile. Profile data: [width, height, web thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","W","Draft",QT_TRANSLATE_NOOP("App::Property","W of the beam")).W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).H = profile[5]
        obj.addProperty("App::PropertyLength","t1","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the webs")).t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the webs")).t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        import Part
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        p1 = Vector(-W/2,-H/2,0)
        p2 = Vector(W/2,-H/2,0)
        p3 = Vector(W/2,H/2,0)
        p4 = Vector(W/2-t1,H/2,0)
        p5 = Vector(W/2-t1,t2-H/2,0)
        p6 = Vector(-W/2,t2-H/2,0)        
        p = Part.makePolygon([p1,p2,p3,p4,p5,p6,p1])
        s = Part.Face(p)
        # v=s.CenterOfMass.negative() 
        # s.translate(v) # to move the c.o.m. in (0,0,0). Why does it not work?
        obj.Shape = s

class _ProfileT(_Profile):
    '''A parametric T beam profile. Profile data: [width, height, web thickness]'''
    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","W","Draft",QT_TRANSLATE_NOOP("App::Property","W of the beam")).W = profile[4]
        obj.addProperty("App::PropertyLength","H","Draft",QT_TRANSLATE_NOOP("App::Property","H of the beam")).H = profile[5]
        obj.addProperty("App::PropertyLength","t1","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web")).t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web")).t2 = profile[7]
        _Profile.__init__(self,obj,profile)
    def execute(self,obj):
        import Part
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        p1 = Vector(-W/2,-H/2,0)
        p2 = Vector(W/2,-H/2,0)
        p3 = Vector(W/2,(-H/2)+t2,0)
        p4 = Vector(t1/2,(-H/2)+t2,0)
        p5 = Vector(t1/2,H/2,0)
        p6 = Vector(-t1/2,H/2,0)
        p7 = Vector(-t1/2,(-H/2)+t2,0)
        p8 = Vector(-W/2,(-H/2)+t2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p5,p6,p7,p8,p1])
        s = Part.Face(p)
        obj.Shape = s

class _ProfileZ(_Profile):
    '''A parametric Z beam profile. Profile data: [width, height, web thickness, flange thickness]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","W","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).W = profile[5]
        obj.addProperty("App::PropertyLength","H","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).H = profile[4]
        obj.addProperty("App::PropertyLength","t1","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web")).t1 = profile[6]
        obj.addProperty("App::PropertyLength","t2","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the flanges")).t2 = profile[7]
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        W, H, t1, t2= obj.W.Value, obj.H.Value, obj.t1.Value, obj.t2.Value
        pl = obj.Placement
        p1 = Vector(-t1/2,-W/2,0)
        p2 = Vector(-t1/2,(W/2)-t2,0)
        p3 = Vector(t1/2-H,(W/2)-t2,0)
        p4 = Vector(t1/2-H,W/2,0)
        p5 = Vector(t1/2,W/2,0)
        p6 = Vector(t1/2,t2-W/2,0)
        p7 = Vector(H-t1/2,t2-W/2,0)
        p8 = Vector(H-t1/2,-W/2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p5,p6,p7,p8,p1])
        p = Part.Face(p)
        obj.Shape = p
        obj.Placement = pl		

class _ProfileCC(_Profile):
    '''A parametric C beam profile. Profile data: [width, height, web thickness, flange thickness]'''

    def __init__(self,obj, profile):
        obj.addProperty("App::PropertyLength","Width","Draft",QT_TRANSLATE_NOOP("App::Property","Width of the beam")).Width = profile[4]
        obj.addProperty("App::PropertyLength","Height","Draft",QT_TRANSLATE_NOOP("App::Property","Height of the beam")).Height = profile[5]
        obj.addProperty("App::PropertyLength","Thickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the web")).Thickness = profile[6]
        obj.addProperty("App::PropertyLength","FlangeThickness","Draft",QT_TRANSLATE_NOOP("App::Property","Thickness of the flanges")).FlangeThickness = profile[7]
        _Profile.__init__(self,obj,profile)

    def execute(self,obj):
        import Part
        pl = obj.Placement
        p1 = Vector(-obj.Height.Value/2,-obj.Width.Value/2,0)
        p2 = Vector(-obj.Height.Value/2,obj.Width.Value/2,0)
        p3 = Vector(obj.Height.Value/2,obj.Width.Value/2,0) 
        p4 = Vector(obj.Height.Value/2,obj.Width.Value/2-obj.Thickness.Value,0)
        p5 = Vector(obj.Height.Value/2-obj.FlangeThickness.Value,obj.Width.Value/2-obj.Thickness.Value,0)
        p6 = Vector(obj.Height.Value/2-obj.FlangeThickness.Value,obj.Width.Value/2-obj.FlangeThickness.Value,0)
        p7 = Vector(obj.FlangeThickness.Value-obj.Height.Value/2,obj.Width.Value/2-obj.FlangeThickness.Value,0)
        p8 = Vector(obj.FlangeThickness.Value-obj.Height.Value/2,obj.FlangeThickness.Value-obj.Width.Value/2,0)
        p9 = Vector(obj.Height.Value/2-obj.FlangeThickness.Value,obj.FlangeThickness.Value-obj.Width.Value/2,0)
        p10 = Vector(obj.Height.Value/2-obj.FlangeThickness.Value,obj.Thickness.Value-obj.Width.Value/2,0)
        p11 = Vector(obj.Height.Value/2,obj.Thickness.Value-obj.Width.Value/2,0)
        p12 = Vector(obj.Height.Value/2,-obj.Width.Value/2,0)
        p = Part.makePolygon([p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p1])
        s = Part.Face(p)
        obj.Shape = s
