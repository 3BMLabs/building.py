# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2023 Maarten Vroegindeweij & Jonathan van der Gouwe      *
#*   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
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

from geometry.point import *
from geometry.curve import *
from abstract.text import *
"""This module provides tools for analytical element like supports, loads
"""

__title__= "annotation"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/annotation.py"

class Dimension:
    def __init__(self, start: Point, end: Point) -> None:
        self.start: Point = start
        self.end: Point = end
        self.id = helper.generateID()
        self.scale = 0.01

#    def geom:

class DimensionType:
    def __init__(self):
        self.name: Point = None
        self.id = helper.generateID()
        self.font = None
      #  self.


class FrameTag:
    def __init__(self):
        # Dimensions in 1/100 scale
        self.scale = 0.1
        self.cs: CoordinateSystem = CSGlobal
        self.offset_from_start = 500
        # self.textoff_vector_local: Vector3 = Vector3(self.width/5,self.height*0.8,0)
        self.textoff_vector_local: Vector3 = Vector3(1, 1, 1)
        self.font_family = "calibri"
        self.text: str = "text"
        self.textheight = 2.5
        self.textcurves = None

    def __textobject(self):
        cstext = self.cs
        # cstextnew = cstext.translate(self.textoff_vector_local)
        self.textcurves = Text(text=self.text, font_family=self.font_family, cs=cstext, scale=self.scale).write

    def by_cs_text(self, coordinate_system: CoordinateSystem, text):
        self.cs = coordinate_system
        self.text = text
        self.__textobject()
        return self

    def write(self, project):
        for x in self.textcurves():
            project.objects.append(x)
        return self
    @staticmethod
    def by_frame(frame):
        tag = FrameTag()
        frame_vector = frame.vector_normalised
        x = frame_vector
        y = Vector3.rotateXY(x,math.radians(90))
        z = ZAxis
        v = Vector3.scale(frame_vector,tag.offset_from_start)
        origintext = Point.translate(frame.start,v)
        csnew = CoordinateSystem(origintext,x,y,z)
        print(csnew)
        tag.cs = csnew
        tag.text = frame.name
        tag.__textobject()
        return tag
class ColumnTag:
    def __init__(self):
        #Dimensions in 1/100 scale
        self.width = 700
        self.height = 500
        self.factor = 3
        self.scale = 0.1
        self.cs: CoordinateSystem = CSGlobal
       # self.textoff_vector_local: Vector3 = Vector3(self.width/5,self.height*0.8,0)
        self.textoff_vector_local: Vector3 = Vector3(1,1,1)

        self.font_family = "calibri"
        self.curves = []
        #self.leadercurves()
        self.text: str = "text"
        self.textheight = 2.5
        self.textcurves = None
        #self.textobject()


    def __leadercurves(self):
        self.startpoint = Point(0,0,0)
        self.midpoint = Point.translate(self.startpoint, Vector3(self.height/self.factor, self.height,0))
        self.endpoint = Point.translate(self.midpoint,Vector3(self.width,0,0))
        crves = [Line(start=self.startpoint,end=self.midpoint), Line(start=self.midpoint,end=self.endpoint)]
        for i in crves:
            j = Line.transform(i,self.cs)
            self.curves.append(j)


    def __textobject(self):
        cstext = self.cs
        #cstextnew = cstext.translate(self.textoff_vector_local)
        self.textcurves = Text(text=self.text, font_family=self.font_family, cs=cstext, scale=self.scale).write


    def by_cs_text(self,coordinate_system: CoordinateSystem, text):
        self.cs = coordinate_system
        self.text = text
        self.__leadercurves()
        self.__textobject()
        return self


    def write(self,project):
        for x in self.textcurves():
            project.objects.append(x)
        for y in self.curves:
            project.objects.append(y)

    @staticmethod
    def by_frame(frame):
        tag = ColumnTag()
        csold = CSGlobal
        tag.cs = CoordinateSystem.translate(csold,Vector3(frame.start.x,frame.start.y,frame.start.z))
        tag.text = frame.name
        tag.__leadercurves()
        tag.__textobject()
        return tag


#class Label:
#class LabelType:
#class TextType: