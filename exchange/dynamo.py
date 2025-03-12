

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point as pnt
from Autodesk.DesignScript.Geometry import Line as ln
from Autodesk.DesignScript.Geometry import Arc as ac
from Autodesk.DesignScript.Geometry import PolyCurve as pc


#AUTODESK DESIGNSCRIPT TO BUILDINGPY
def DesignScriptPointToBPPoint(DesignScriptPoint):
    BPPoint = Point(DesignScriptPoint.X,DesignScriptPoint.Y,DesignScriptPoint.Z)
    return BPPoint

#BUILDINGPY TO AUTODESK DESIGNSCRIPT

def BPPointToDesignScriptPoint(BPPoint):
    DesignScriptPoint = pnt.ByCoordinates(BPPoint.x,BPPoint.y,BPPoint.z)
    return DesignScriptPoint

def BPArcToDesignScriptArc(BPArc):
    p1 = BPPointToDesignScriptPoint(BPArc.start)
    p2 = BPPointToDesignScriptPoint(BPArc.mid)
    p3 = BPPointToDesignScriptPoint(BPArc.end)

    DesignScriptArc = ac.ByThreePoints(p1,p2,p3)
    return DesignScriptArc

def BPLineToDesignScriptLine(BPLine):
    p1 = BPPointToDesignScriptPoint(BPLine.start)
    p2 = BPPointToDesignScriptPoint(BPLine.end)

    DesignScriptLine = ln.ByStartPointEndPoint(p1,p2)
    return DesignScriptLine

def BPPolyCurveToDesignScriptPolyCurve(BPPolyCurve):
    DesignScriptCurves = []

    for curve in BPPolyCurve.curves:
        nm = curve.__class__.__name__
        if nm == 'Arc':
            DesignScriptCurves.append(
                BPArcToDesignScriptArc(curve)
            )
        elif nm == 'Line':
            DesignScriptCurves.append(
                BPLineToDesignScriptLine(curve)
            )
    DesignScriptPolyCurve = pc.ByJoinedCurves(DesignScriptCurves)
    return DesignScriptPolyCurve