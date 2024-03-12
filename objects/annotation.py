# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
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

from abstract.text import *
"""This module provides tools for annotations like text, label, dimension, dimension tick etc
"""

__title__= "annotation"
__author__ = "Maarten & Jonathan"
__url__ = "./objects/annotation.py"

# [!not included in BP singlefile - end]

class TickMark:
    #Dimension Tick Mark
    def __init__(self):
        self.name = None
        self.id = generateID()
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
        self.id = generateID()
        self.type = __class__.__name__
        self.font = None
        self.text_height = 2.5
        self.tick_mark: TickMark = TMDiagonal
        self.line_extension = 100

    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
            'type': self.type,
            'font': self.font,
            'text_height': self.text_height,
            'tick_mark': str(self.tick_mark),
            'line_extension': self.line_extension
        }
    
    @staticmethod
    def deserialize(data):
        dimension_type = DimensionType()
        dimension_type.name = data.get('name')
        dimension_type.id = data.get('id')
        dimension_type.type = data.get('type')
        dimension_type.font = data.get('font')
        dimension_type.text_height = data.get('text_height', 2.5)
        
        # Handle TickMark deserialization
        tick_mark_str = data.get('tick_mark')
        dimension_type.tick_mark = TickMark(tick_mark_str)  # Adjust according to your TickMark implementation

        dimension_type.line_extension = data.get('line_extension', 100)

        return dimension_type

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
        self.id = generateID()
        self.type = __class__.__name__
        self.start: Point = start
        self.text_height = 100
        self.end: Point = end
        self.scale = 0.1 #text
        self.dimension_type: DimensionType = dimension_type
        self.curves = []
        self.length: float = Line(start=self.start,end=self.end).length
        self.text = None
        self.geom()

    def serialize(self):
        return {
            'type': self.type,
            'start': self.start.serialize(),
            'end': self.end.serialize(),
            'text_height': self.text_height,
            'id': self.id,
            'scale': self.scale,
            'dimension_type': self.dimension_type.serialize(),
            'curves': [curve.serialize() for curve in self.curves],
            'length': self.length,
            'text': self.text
        }

    @staticmethod
    def deserialize(data):
        start = Point.deserialize(data['start'])
        end = Point.deserialize(data['end'])
        dimension_type = DimensionType.deserialize(data['dimension_type'])
        dimension = Dimension(start, end, dimension_type)

        dimension.text_height = data.get('text_height', 100)
        dimension.id = data.get('id')
        dimension.scale = data.get('scale', 0.1)
        dimension.curves = [Line.deserialize(curve_data) for curve_data in data.get('curves', [])]
        dimension.length = data.get('length')
        dimension.text = data.get('text')

        return dimension

    @staticmethod
    def by_startpoint_endpoint_offset(start:Point,end:Point,dimension_type: DimensionType, offset: float):
        DS = Dimension()
        DS.start = start
        DS.end = end
        DS.dimension_type = dimension_type
        DS.geom()
        return DS

    def geom(self):
        #baseline
        baseline = Line(start=self.start,end=self.end)
        midpoint_text = baseline.mid_point()
        direction = Vector3.normalize(baseline.vector)
        tick_mark_extension_point_1 = Point.translate(self.start,Vector3.reverse(Vector3.scale(direction,self.dimension_type.line_extension)))
        tick_mark_extension_point_2 = Point.translate(self.end,Vector3.scale(direction,self.dimension_type.line_extension))
        x = direction
        y = Vector3.rotate_XY(x, math.radians(90))
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
        self.text = Text(text=str(round(self.length)), font_family=self.dimension_type.font, cs=cs_new_mid, height=self.text_height).write()

    def write(self,project):
        for i in self.curves:
            project.objects.append(i)
        for j in self.text:
            project.objects.append(j)


class FrameTag:
    def __init__(self):
        # Dimensions in 1/100 scale
        self.id = generateID()
        self.type = __class__.__name__
        self.scale = 0.1
        self.cs: CoordinateSystem = CSGlobal
        self.offset_x = 500
        self.offset_y = 100
        self.font_family = "calibri"
        self.text: str = "text"
        self.text_curves = None
        self.text_height = 100

    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'scale': self.scale,
            'cs': self.cs.serialize(),
            'offset_x': self.offset_x,
            'offset_y': self.offset_y,
            'font_family': self.font_family,
            'text': self.text,
            'text_curves': self.text_curves,
            'text_height': self.text_height
        }
    
    @staticmethod
    def deserialize(data):
        frame_tag = FrameTag()
        frame_tag.scale = data.get('scale', 0.1)
        frame_tag.cs = CoordinateSystem.deserialize(data['cs'])
        frame_tag.offset_x = data.get('offset_x', 500)
        frame_tag.offset_y = data.get('offset_y', 100)
        frame_tag.font_family = data.get('font_family', "calibri")
        frame_tag.text = data.get('text', "text")
        frame_tag.text_curves = data.get('text_curves')
        frame_tag.text_height = data.get('text_height', 100)

        return frame_tag

    def __textobject(self):
        cstext = self.cs
        # cstextnew = cstext.translate(self.textoff_vector_local)
        self.text_curves = Text(text=self.text, font_family=self.font_family, height=self.text_height, cs=cstext).write

    def by_cs_text(self, coordinate_system: CoordinateSystem, text):
        self.cs = coordinate_system
        self.text = text
        self.__textobject()
        return self

    def write(self, project):
        for x in self.text_curves():
            project.objects.append(x)
        return self

    @staticmethod
    def by_frame(frame):
        tag = FrameTag()
        frame_vector = frame.vector_normalised
        x = frame_vector
        y = Vector3.rotate_XY(x,math.radians(90))
        z = ZAxis
        vx = Vector3.scale(frame_vector,tag.offset_x)
        frame_width = PolyCurve2D.bounds(frame.curve)[4]
        vy = Vector3.scale(y,frame_width*0.5+tag.offset_y)
        origintext = Point.translate(frame.start,vx)
        origintext = Point.translate(origintext,vy)
        csnew = CoordinateSystem(origintext,x,y,z)
        tag.cs = csnew
        tag.text = frame.name
        tag.__textobject()
        return tag


class ColumnTag:
    def __init__(self):
        #Dimensions in 1/100 scale
        self.id = generateID()
        self.type = __class__.__name__
        self.width = 700
        self.height = 500
        self.factor = 3 #hellingsfacor leader
        self.scale = 0.1 #voor tekeningverschaling
        self.position = "TL"  # TL, TR, BL, BR Top Left Top Right Bottom Left Bottom Right
        self.cs: CoordinateSystem = CSGlobal

        #self.textoff_vector_local: Vector3 = Vector3(1,1,1)
        self.font_family = "calibri"
        self.curves = []
        #self.leadercurves()
        self.text: str = "text"
        self.text_height = 100
        self.text_offset_factor = 5
        self.textoff_vector_local: Vector3 = Vector3(self.height/self.factor,self.height+self.height/self.text_offset_factor,0)
        self.text_curves = None
        #self.textobject()

    def serialize(self):
        id_value = str(self.id) if not isinstance(self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type' : self.type,
            'width': self.width,
            'height': self.height,
            'factor': self.factor,
            'scale': self.scale,
            'position': self.position,
            'cs': self.cs.serialize(),
            'font_family': self.font_family,
            'curves': [curve.serialize() for curve in self.curves],
            'text': self.text,
            'text_height': self.text_height,
            'text_offset_factor': self.text_offset_factor,
            'textoff_vector_local': self.textoff_vector_local.serialize(),
            'text_curves': self.text_curves
        }

    @staticmethod
    def deserialize(data):
        column_tag = ColumnTag()
        column_tag.width = data.get('width', 700)
        column_tag.height = data.get('height', 500)
        column_tag.factor = data.get('factor', 3)
        column_tag.scale = data.get('scale', 0.1)
        column_tag.position = data.get('position', "TL")
        column_tag.cs = CoordinateSystem.deserialize(data['cs'])
        column_tag.font_family = data.get('font_family', "calibri")
        column_tag.curves = [Line.deserialize(curve_data) for curve_data in data.get('curves', [])]
        column_tag.text = data.get('text', "text")
        column_tag.text_height = data.get('text_height', 100)
        column_tag.text_offset_factor = data.get('text_offset_factor', 5)
        column_tag.textoff_vector_local = Vector3.deserialize(data['textoff_vector_local'])
        column_tag.text_curves = data.get('text_curves')

        return column_tag

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

        cstextnew = CoordinateSystem.translate(cstext,self.textoff_vector_local)
        self.text_curves = Text(text=self.text, font_family=self.font_family, height=self.text_height, cs=cstextnew).write

    def by_cs_text(self,coordinate_system: CoordinateSystem, text):
        self.cs = coordinate_system
        self.text = text
        self.__leadercurves()
        self.__textobject()
        return self

    def write(self,project):
        for x in self.text_curves():
            project.objects.append(x)
        for y in self.curves:
            project.objects.append(y)

    @staticmethod
    def by_frame(frame, position= "TL"):
        tag = ColumnTag()
        csold = CSGlobal
        tag.position = position
        tag.cs = CoordinateSystem.translate(csold,Vector3(frame.start.x,frame.start.y,frame.start.z))
        tag.text = frame.name
        tag.__leadercurves()
        tag.__textobject()
        return tag

#class Label:
#class LabelType:
#class TextType: