# [included in BP singlefile]
# [!not included in BP singlefile - start]
# -*- coding: utf8 -*-
# ***************************************************************************
# *   Copyright (c) 2024 Maarten Vroegindeweij & Jonathan van der Gouwe      *
# *   maarten@3bm.co.nl & jonathan@3bm.co.nl                                *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************


"""This module provides tools to create solids
"""

__title__ = "solid"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/solid.py"


import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from geometry.curve import *
from geometry.geometry2d import PolyCurve2D
from abstract.plane import *
import packages.helper as helper


# [!not included in BP singlefile - end]


class Extrusion:
    # Extrude a 2D profile to a 3D mesh or solid
    """The Extrusion class represents the process of extruding a 2D profile into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process."""
    def __init__(self):
        """The Extrusion class represents the process of extruding a 2D profile into a 3D mesh or solid form. It is designed to handle geometric transformations and properties related to the extrusion process.
        
        - `id` (str): A unique identifier for the extrusion instance.
        - `type` (str): Class name, indicating the object type as "Extrusion".
        - `parameters` (list): A list of parameters associated with the extrusion.
        - `verts` (list): A list of vertices that define the shape of the extruded mesh.
        - `faces` (list): A list of faces, each defined by indices into the `verts` list.
        - `numberFaces` (int): The total number of faces in the extrusion.
        - `countVertsFaces` (int): The total number of vertices per face, distinct from the total vertex count.
        - `name` (str): The name assigned to the extrusion instance.
        - `color` (tuple): The color of the extrusion, defined as an RGB tuple.
        - `colorlst` (list): A list of colors applied to the extrusion, potentially varying per face or vertex.
        - `topface` (PolyCurve): The top face of the extrusion, returned as a polycurve converted to a surface.
        - `bottomface` (PolyCurve): The bottom face of the extrusion, similar to `topface`.
        - `polycurve_3d_translated` (PolyCurve): A polycurve representing the translated 3D profile of the extrusion.
        - `bottomshape` (list): A list representing the shape of the bottom face of the extrusion.
        """
        self.id = generateID()
        self.type = __class__.__name__
        self.parameters = []
        self.verts = []
        self.faces = []
        self.numberFaces = 0
        # total number of verts per face (not the same as total verts)
        self.countVertsFaces = 0
        self.name = None
        self.color = (255, 255, 0)
        self.colorlst = []
        self.topface = None  # return polycurve -> surface
        self.bottomface = None  # return polycurve -> surface
        self.polycurve_3d_translated = None
        self.outercurve = []
        self.bottomshape = []
        self.nested = []

    def serialize(self) -> dict:
        """Serializes the extrusion object into a dictionary.
        This method facilitates the conversion of the Extrusion instance into a dictionary format, suitable for serialization to JSON or other data formats for storage or network transmission.

        #### Returns:
        `dict`: A dictionary representation of the Extrusion instance, including all relevant geometric and property data.
    
        #### Example usage:
        ```python

        ```
        """
        id_value = str(self.id) if not isinstance(
            self.id, (str, int, float)) else self.id
        return {
            'id': id_value,
            'type': self.type,
            'verts': self.verts,
            'faces': self.faces,
            'numberFaces': self.numberFaces,
            'countVertsFaces': self.countVertsFaces,
            'name': self.name,
            'color': self.color,
            'colorlst': self.colorlst,
            'topface': self.topface.serialize() if self.topface else None,
            'bottomface': self.bottomface.serialize() if self.bottomface else None,
            'polycurve_3d_translated': self.polycurve_3d_translated.serialize() if self.polycurve_3d_translated else None
        }

    @staticmethod
    def deserialize(data: dict) -> 'Extrusion':
        """Reconstructs an Extrusion object from a dictionary.
        This static method allows for the creation of an Extrusion instance from serialized data, enabling the loading of extrusion objects from file storage or network data.

        #### Parameters:
        - `data` (dict): A dictionary containing serialized Extrusion data.

        #### Returns:
        `Extrusion`: A newly constructed Extrusion instance based on the provided data.
    
        #### Example usage:
        ```python

        ```
        """
        extrusion = Extrusion()
        extrusion.id = data.get('id')
        extrusion.verts = data.get('verts', [])
        extrusion.faces = data.get('faces', [])
        extrusion.numberFaces = data.get('numberFaces', 0)
        extrusion.countVertsFaces = data.get('countVertsFaces', 0)
        extrusion.name = data.get('name', "none")
        extrusion.color = data.get('color', (255, 255, 0))
        extrusion.colorlst = data.get('colorlst', [])

        if data.get('topface'):
            extrusion.topface = PolyCurve.deserialize(data['topface'])

        if data.get('bottomface'):
            extrusion.bottomface = PolyCurve.deserialize(data['bottomface'])

        if data.get('polycurve_3d_translated'):
            extrusion.polycurve_3d_translated = PolyCurve.deserialize(
                data['polycurve_3d_translated'])

        return extrusion

    def set_parameter(self, data: list) -> 'Extrusion':
        """Sets parameters for the extrusion.
        This method allows for the modification of the Extrusion's parameters, which can influence the extrusion process or define additional properties.

        #### Parameters:
        - `data` (list): A list of parameters to be applied to the extrusion.

        #### Returns:
        `Extrusion`: The Extrusion instance with updated parameters.
    
        #### Example usage:
        ```python

        ```
        """
        self.parameters = data
        return self

    @staticmethod
    def merge(extrusions: list, name: str = None) -> 'Extrusion':
        """Merges multiple Extrusion instances into a single one.
        This class method combines several extrusions into a single Extrusion object, potentially useful for operations requiring unified geometric manipulation.

        #### Parameters:
        - `extrusions` (list): A list of Extrusion instances to be merged.
        - `name` (str, optional): The name for the merged extrusion.

        #### Returns:
        `Extrusion`: A new Extrusion instance resulting from the merger of the provided extrusions.
    
        #### Example usage:
        ```python

        ```
        """
        Outrus = Extrusion()
        if isinstance(extrusions, list):
            Outrus.verts = []
            Outrus.faces = []
            Outrus.colorlst = []
            for ext in extrusions:
                Outrus.verts.append(ext.verts)
                Outrus.faces.append(ext.faces)
                Outrus.colorlst.append(ext.colorlst)
            Outrus.verts = flatten(Outrus.verts)
            Outrus.faces = flatten(Outrus.faces)
            Outrus.colorlst = flatten(Outrus.colorlst)
            return Outrus

        elif isinstance(extrusions, Extrusion):
            return extrusions

    @staticmethod
    def by_polycurve_height_vector(polycurve_2d: PolyCurve2D, height: float, cs_old: CoordinateSystem, start_point: Point, direction_vector: Vector3) -> 'Extrusion':
        """Creates an extrusion from a 2D polycurve profile along a specified vector.
        This method extrudes a 2D polycurve profile into a 3D form by translating it to a specified start point and direction. The extrusion is created perpendicular to the polycurve's plane, extending it to the specified height.

        #### Parameters:
        - `polycurve_2d` (PolyCurve2D): The 2D polycurve to be extruded.
        - `height` (float): The height of the extrusion.
        - `cs_old` (CoordinateSystem): The original coordinate system of the polycurve.
        - `start_point` (Point): The start point for the extrusion in the new coordinate system.
        - `direction_vector` (Vector3): The direction vector along which the polycurve is extruded.

        #### Returns:
        `Extrusion`: An Extrusion object representing the 3D form of the extruded polycurve.

        #### Example usage:
        ```python
        extrusion = Extrusion.by_polycurve_height_vector(polycurve_2d, 10, oldCS, startPoint, directionVec)
        ```
        """
        Extrus = Extrusion()
        # 2D PolyCurve @ Global origin
        count = 0

        Extrus.polycurve_3d_translated = PolyCurve.transform_from_origin(
            polycurve_2d, start_point, direction_vector)

        try:
            for i in polycurve_2d.curves:
                startpointLow = transform_point(
                    Point(i.start.x, i.start.y, 0), cs_old, start_point, direction_vector)
                endpointLow = transform_point(
                    Point(i.end.x, i.end.y, 0), cs_old, start_point, direction_vector)
                endpointHigh = transform_point(
                    Point(i.end.x, i.end.y, height), cs_old, start_point, direction_vector)
                startpointHigh = transform_point(
                    Point(i.start.x, i.start.y, height), cs_old, start_point, direction_vector)

                # Construct faces perpendicular on polycurve
                Extrus.faces.append(4)
                Extrus.verts.append(startpointLow.x)
                Extrus.verts.append(startpointLow.y)
                Extrus.verts.append(startpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointLow.x)
                Extrus.verts.append(endpointLow.y)
                Extrus.verts.append(endpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointHigh.x)
                Extrus.verts.append(endpointHigh.y)
                Extrus.verts.append(endpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(startpointHigh.x)
                Extrus.verts.append(startpointHigh.y)
                Extrus.verts.append(startpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.numberFaces = Extrus.numberFaces + 1

            # bottomface
            Extrus.faces.append(len(polycurve_2d.curves))

            count = 0
            for i in polycurve_2d.curves:
                Extrus.faces.append(count)
                Extrus.bottomshape.append(i)
                count = count + 4

            # topface
            Extrus.faces.append(len(polycurve_2d.curves))
            count = 3
            for i in polycurve_2d.curves:
                Extrus.faces.append(count)
                count = count + 4
        except:
            for i in polycurve_2d.curves:
                startpointLow = transform_point(
                    Point(i.start.x, i.start.y, 0), cs_old, start_point, direction_vector)
                endpointLow = transform_point(
                    Point(i.end.x, i.end.y, 0), cs_old, start_point, direction_vector)
                endpointHigh = transform_point(
                    Point(i.end.x, i.end.y, height), cs_old, start_point, direction_vector)
                startpointHigh = transform_point(
                    Point(i.start.x, i.start.y, height), cs_old, start_point, direction_vector)

                # Construct faces perpendicular on polycurve
                Extrus.faces.append(4)
                Extrus.verts.append(startpointLow.x)
                Extrus.verts.append(startpointLow.y)
                Extrus.verts.append(startpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointLow.x)
                Extrus.verts.append(endpointLow.y)
                Extrus.verts.append(endpointLow.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(endpointHigh.x)
                Extrus.verts.append(endpointHigh.y)
                Extrus.verts.append(endpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.verts.append(startpointHigh.x)
                Extrus.verts.append(startpointHigh.y)
                Extrus.verts.append(startpointHigh.z)
                Extrus.faces.append(count)
                count += 1
                Extrus.numberFaces = Extrus.numberFaces + 1

            # bottomface
            Extrus.faces.append(len(polycurve_2d.curves))

            count = 0
            for i in polycurve_2d.curves:
                Extrus.faces.append(count)
                Extrus.bottomshape.append(i)
                count = count + 4

            # topface
            Extrus.faces.append(len(polycurve_2d.curves))
            count = 3
            for i in polycurve_2d.curves:
                Extrus.faces.append(count)
                count = count + 4

        Extrus.countVertsFaces = (4 * Extrus.numberFaces)

        Extrus.countVertsFaces = Extrus.countVertsFaces + \
            len(polycurve_2d.curves)*2
        Extrus.numberFaces = Extrus.numberFaces + 2

        Extrus.outercurve = polycurve_2d

        for j in range(int(len(Extrus.verts) / 3)):
            Extrus.colorlst.append(Extrus.color)

        return Extrus

    @staticmethod
    def by_polycurve_height(polycurve: PolyCurve, height: float, dz_loc: float) -> 'Extrusion':
        """Creates an extrusion from a PolyCurve with a specified height and base elevation.
        This method generates a vertical extrusion of a given PolyCurve. The PolyCurve is first translated vertically by `dz_loc`, then extruded to the specified `height`, creating a solid form.

        #### Parameters:
        - `polycurve` (PolyCurve): The PolyCurve to be extruded.
        - `height` (float): The height of the extrusion.
        - `dz_loc` (float): The base elevation offset from the original plane of the PolyCurve.

        #### Returns:
        `Extrusion`: An Extrusion object that represents the 3D extruded form of the input PolyCurve.

        #### Example usage:
        ```python
        extrusion = Extrusion.by_polycurve_height(polycurve, 5, 0)
        ```
        """
        # global len
        Extrus = Extrusion()
        Points = polycurve.points
        V1 = Vector3.by_two_points(Points[0], Points[1])
        V2 = Vector3.by_two_points(Points[-2], Points[-1])

        p1 = Plane.by_two_vectors_origin(
            V1, V2, Points[0])  # Workplane of PolyCurve
        norm = p1.Normal

        pnts = []
        faces = []

        Extrus.polycurve_3d_translated = polycurve

        # allverts
        for pnt in Points:
            # Onderzijde verplaatst met dz_loc
            pnts.append(Point.translate(pnt, Vector3.product(dz_loc, norm)))
        for pnt in Points:
            # Bovenzijde verplaatst met dz_loc
            pnts.append(Point.translate(
                pnt, Vector3.product((dz_loc+height), norm)))

        numPoints = len(Points)

        # Bottomface
        count = 0
        face = []
        for x in range(numPoints):
            face.append(count)
            count = count + 1
        faces.append(face)

        # Topface
        count = 0
        face = []
        for x in range(numPoints):
            face.append(count+numPoints)
            count = count + 1
        faces.append(face)

        # Sides
        count = 0
        length = len(faces[0])
        for i, j in zip(faces[0], faces[1]):
            face = []
            face.append(i)
            face.append(faces[0][count + 1])
            face.append(faces[1][count + 1])
            face.append(j)
            count = count + 1
            if count == length-1:
                face.append(i)
                face.append(faces[0][0])
                face.append(faces[1][0])
                face.append(j)
                faces.append(face)
                break
            else:
                pass
            faces.append(face)

        # toMeshStructure
        for i in pnts:
            Extrus.verts.append(i.x)
            Extrus.verts.append(i.y)
            Extrus.verts.append(i.z)

        for x in faces:
            Extrus.faces.append(len(x))  # Number of verts in face
            for y in x:
                Extrus.faces.append(y)

        Extrus.numberFaces = len(faces)
        Extrus.countVertsFaces = (4 * len(faces))

        for j in range(int(len(Extrus.verts) / 3)):
            Extrus.colorlst.append(Extrus.color)
        return Extrus
