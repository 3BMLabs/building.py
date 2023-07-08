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
"""This module provides tools for annotations like text, label, dimension, dimension tick etc
"""

__title__= "annotation"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/annotation.py"

class TickMark:
    #Dimension Tick Mark
    def __init(self):
        self.name = None
        self.id = helper.generateID()
        self.curves = []

    @staticmethod
    def by_curves(name,curves):
        TM = TickMark()
        TM.name = name
        TM.curves = curves
        return TM

TMDiagonal = TickMark.by_curves("diagonal",[Line(start = Point(-100,-100,0),end = Point(100,100,0))])

class DimensionType:
    def __init__(self):
        self.name = None
        self.id = helper.generateID()
        self.font = None
        self.text_height = 2.5
        self.tick_mark: TickMark = TMDiagonal
        self.line_extension = 100

    @staticmethod
    def by_name_font_textheight_tick_mark_extension(name: str,font: str,text_height: float,tick_mark: TickMark,line_extension:float):
        DT = DimensionType()
        DT.name = name
        DT.font = font
        DT.text_height = text_height
        DT.tick_mark = tick_mark
        DT.line_extension = line_extension
        return DT


DT2_5_mm = DimensionType.by_name_font_textheight_tick_mark_extension("2.5 mm","calibri",2.5,TMDiagonal,100)

DT1_8_mm = DimensionType.by_name_font_textheight_tick_mark_extension("1.8 mm","calibri",2.5,TMDiagonal,100)

class Dimension:
    def __init__(self, start: Point, end: Point, dimension_type) -> None:
        self.start: Point = start
        self.end: Point = end
        self.id = helper.generateID()
        self.scale = 0.1 #text
        self.dimension_type: DimensionType = dimension_type
        self.curves = []
        self.length: float = Line(start=self.start,end=self.end).length
        self.text = None
        self.geom()
    def geom(self):
        #baseline
        baseline = Line(start=self.start,end=self.end)
        midpoint_text = baseline.mid_point()
        direction = Vector3.normalize(baseline.vector)
        tick_mark_extension_point_1 = Point.translate(self.start,Vector3.reverse(Vector3.scale(direction,self.dimension_type.line_extension)))
        tick_mark_extension_point_2 = Point.translate(self.end,Vector3.scale(direction,self.dimension_type.line_extension))
        x = direction
        y = Vector3.rotateXY(x, math.radians(90))
        z = ZAxis
        cs_new_start = CoordinateSystem(self.start,x,y,z)
        cs_new_mid = CoordinateSystem(midpoint_text, x, y, z)
        cs_new_end = CoordinateSystem(self.end,x,y,z)
        self.curves.append(Line(tick_mark_extension_point_1,self.start)) #extention_start
        self.curves.append(Line(tick_mark_extension_point_2,self.end)) #extention_end
        self.curves.append(Line(self.start,self.end)) #baseline
        crvs = Line(start = self.dimension_type.tick_mark.curves[0].start,end = self.dimension_type.tick_mark.curves[0].end) #erg vieze oplossing. #Todo
        self.curves.append(Line.transform(self.dimension_type.tick_mark.curves[0], cs_new_start)) #dimension tick start
        self.curves.append(Line.transform(crvs, cs_new_end))  #dimension tick end
        self.text = Text(text=str(round(self.length)), font_family=self.dimension_type.font, cs=cs_new_mid, scale=self.scale).write()

    def write(self,project):
        for i in self.curves:
            project.objects.append(i)
        for j in self.text:
            project.objects.append(j)


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