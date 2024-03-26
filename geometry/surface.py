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


"""This module provides tools to create surfaces
"""

__title__ = "surface"
__author__ = "Maarten & Jonathan"
__url__ = "./geometry/surface.py"


import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.curve import *
from geometry.solid import Extrusion
from abstract.color import Color
from abstract.intersect2d import *


# [!not included in BP singlefile - end]
# check if there are innercurves inside the outer curve.


class Surface:
    """Represents a surface object created from PolyCurves."""
    def __init__(self, PolyCurves: PolyCurve, color=None) -> None:
        """This class is designed to manage and manipulate surfaces derived from PolyCurve objects. It supports the generation of mesh representations, serialization/deserialization, and operations like filling and voiding based on PolyCurve inputs.
       
        - `type` (str): The class name, "Surface".
        - `mesh` (list): A list of meshes that represent the surface.
        - `length` (float): The total length of the PolyCurves defining the surface.
        - `area` (float): The area of the surface, excluding any inner PolyCurves.
        - `offset` (float): An offset value for the surface.
        - `name` (str): The name of the surface.
        - `id` (str): A unique identifier for the surface.
        - `PolyCurveList` (list): A list of PolyCurve objects that define the surface.
        - `origincurve` (PolyCurve): The original PolyCurve from which the surface was created.
        - `color` (int): The color of the surface, represented as an integer.
        - `colorlst` (list): A list of color values associated with the surface.
        """
        # self.outerPolyCurve
        # self.innerPolyCurves
        if isinstance(PolyCurves, PolyCurve):
            PolyCurves = [PolyCurves]
        self.type = __class__.__name__
        self.mesh = []
        self.length = 0
        self.area = 0  # return the same area of the polyCurve but remove the innerpolycurves
        self.offset = 0
        self.name = "test2"
        self.id = generateID()
        self.PolyCurveList = PolyCurves
        self.origincurve = None
        if color is None:
            self.color = Color.rgb_to_int(Color().Components("gray"))
        else:
            self.color = color

        self.colorlst = []
        self.fill(self.PolyCurveList)

    def serialize(self) -> dict:
        """Serializes the Surface object into a dictionary for storage or transfer.
        This method converts the Surface object's properties into a dictionary format, making it suitable for serialization processes like saving to a file or sending over a network.

        #### Returns:
        `dict`: A dictionary representation of the Surface object, containing all relevant data such as type, mesh, dimensions, name, ID, PolyCurve list, origin curve, color, and color list.

        #### Example usage:
        ```python
        surface = Surface(polyCurves, color)
        serialized_surface = surface.serialize()
        # serialized_surface is now a dictionary representation of the surface object
        ```
        """
        return {
            'type': self.type,
            'mesh': self.mesh,
            'length': self.length,
            'area': self.area,
            'offset': self.offset,
            'name': self.name,
            'id': self.id,
            'PolyCurveList': [polycurve.serialize() for polycurve in self.PolyCurveList],
            'origincurve': self.origincurve.serialize() if self.origincurve else None,
            'color': self.color,
            'colorlst': self.colorlst
        }

    @staticmethod
    def deserialize(data: dict) -> 'Surface':
        """Creates a Surface object from a serialized data dictionary.
        This static method reconstructs a Surface object from a dictionary containing serialized surface data. It is particularly useful for loading surfaces from storage or reconstructing them from data received over a network.

        #### Parameters:
        - `data` (`dict`): The dictionary containing the serialized data of a Surface object.

        #### Returns:
        `Surface`: A new Surface object initialized with the data from the dictionary.

        #### Example usage:
        ```python
        data = { ... }  # Serialized Surface data
        surface = Surface.deserialize(data)
        # surface is now a fully reconstructed Surface object
        ```
        """
        polycurves = [PolyCurve.deserialize(
            pc_data) for pc_data in data.get('PolyCurveList', [])]
        surface = Surface(polycurves, data.get('color'))

        surface.mesh = data.get('mesh', [])
        surface.length = data.get('length', 0)
        surface.area = data.get('area', 0)
        surface.offset = data.get('offset', 0)
        surface.name = data.get('name', "test2")
        surface.id = data.get('id')
        surface.colorlst = data.get('colorlst', [])

        if data.get('origincurve'):
            surface.origincurve = PolyCurve.deserialize(data['origincurve'])

        return surface

    def fill(self, PolyCurveList: list):
        """Fills the Surface with the specified PolyCurves.
        This method applies PolyCurves to the Surface, creating an extrusion for each PolyCurve and adding it to the surface's mesh. It also assigns the specified color to each extrusion.

        #### Parameters:
        - `PolyCurveList` (`list` or `PolyCurve`): A list of PolyCurve objects or a single PolyCurve object to be applied to the Surface.

        #### Example usage:
        ```python
        polyCurveList = [polyCurve1, polyCurve2]
        surface.fill(polyCurveList)
        # The surface is now filled with the specified PolyCurves.
        ```
        """
        if isinstance(PolyCurveList, PolyCurve):
            plycColorList = []
            p = Extrusion.by_polycurve_height(PolyCurveList, 0, self.offset)
            self.mesh.append(p)
            for j in range(int(len(p.verts) / 3)):
                plycColorList.append(self.color)
            self.colorlst.append(plycColorList)

        elif isinstance(PolyCurveList, list):
            for polyCurve in PolyCurveList:
                plycColorList = []
                p = Extrusion.by_polycurve_height(polyCurve, 0, self.offset)
                self.mesh.append(p)
                for j in range(int(len(p.verts) / 3)):
                    plycColorList.append(self.color)
                self.colorlst.append(plycColorList)

    def void(self, polyCurve: PolyCurve):
        """Creates a void in the Surface based on the specified PolyCurve.
        This method identifies and removes a part of the Surface that intersects with the given PolyCurve, effectively creating a void in the Surface. It then updates the surface's mesh and color list to reflect this change.

        #### Parameters:
        - `polyCurve` (`PolyCurve`): The PolyCurve object that defines the area of the Surface to be voided.

        #### Example usage:
        ```python
        surface.void(polyCurve)
        # A void is now created in the surface based on the specified PolyCurve.
        ```
        """
        # Find the index of the extrusion that intersects with the polyCurve
        idx = None
        for i, extr in enumerate(self.mesh):
            if extr.intersects(polyCurve):
                idx = i
                break

        if idx is not None:
            # Remove the intersected extrusion from the extrusion list
            removed = self.mesh.pop(idx)

            # Remove the corresponding color list from the colorlst list
            removed_colors = self.colorlst.pop(idx)

            # Create a new list of colors for the remaining extrusions
            new_colors = []
            for colors in self.colorlst:
                new_colors.extend(colors)

            # Fill the hole with a new surface
            hole_surface = Surface([polyCurve], color=self.color)
            hole_surface.fill([polyCurve])
            hole_extrusion = hole_surface.extrusion[0]

            # Add the hole extrusion to the extrusion list
            self.mesh.append(hole_extrusion)

            # Add the hole colors to the colorlst list
            hole_colors = [Color.rgb_to_int(Color().Components(
                "red"))] * int(len(hole_extrusion.verts) / 3)
            self.colorlst.append(hole_colors)

            # Add the remaining colors to the colorlst list
            self.colorlst.extend(new_colors)

            # Update the origin curve
            self.origincurve = self.PolyCurveList[0]

    def __id__(self):
        """Returns the unique identifier of the Surface.
        This method provides a way to retrieve the unique ID of the Surface, which can be useful for tracking or identifying surfaces within a larger system.

        #### Returns:
        `str`: The unique identifier of the Surface.

        #### Example usage:
        ```python
        id_str = surface.__id__()
        print(id_str)
        # Outputs the ID of the surface.
        ```
        """

    def __str__(self) -> str:
        """Generates a string representation of the Surface object.
        This method returns a string that includes the class name and optionally additional details about the Surface object, making it easier to identify and distinguish the surface when printed or logged.

        #### Returns:
        `str`: A string representation of the Surface object, typically including its class name and potentially other identifying information.

        #### Example usage:
        ```python
        surface = Surface(polyCurves, color)
        print(surface)
        # Output: Surface({...})
        ```
        """

class NurbsSurface:  # based on point data / degreeU&countU / degreeV&countV?
    """Represents a NURBS (Non-Uniform Rational B-Spline) surface."""
    def __init__(self) -> 'NurbsSurface':
        """NurbsSurface is a mathematical model representing a 3D surface in terms of NURBS, a flexible method to represent curves and surfaces. It encompasses properties such as ID and type but is primarily defined by its control points, weights, and degree in the U and V directions.

        - `id` (str): A unique identifier for the NurbsSurface.
        - `type` (str): Class name, "NurbsSurface".
        """
        self.id = generateID()
        self.type = __class__.__name__

    def __id__(self) -> 'str':
        """Returns the unique identifier of the NurbsSurface object.
        This method provides a standardized way to access the unique ID of the NurbsSurface, useful for identification and tracking purposes within a system that handles multiple surfaces.

        #### Returns:
        `str`: The unique identifier of the NurbsSurface, prefixed with "id:".

        #### Example usage:
        ```python
        nurbs_surface = NurbsSurface()
        print(nurbs_surface.__id__())
        # Output format: "id:{unique_id}"
        ```
        """
        return f"id:{self.id}"

    def __str__(self) -> 'str':
        """Generates a string representation of the NurbsSurface object.
        This method creates a string that summarizes the NurbsSurface, typically including its class name and potentially its unique ID, providing a concise overview of the object when printed or logged.

        #### Returns:
        `str`: A string representation of the NurbsSurface object.

        #### Example usage:
        ```python
        nurbs_surface = NurbsSurface()
        print(nurbs_surface)
        # Output: "NurbsSurface({self})"
        ```
        """
        return f"{__class__.__name__}({self})"


class PolySurface:
    """Represents a compound surface consisting of multiple connected surfaces."""
    def __init__(self) -> None:
        """PolySurface is a geometric entity that represents a complex surface made up of several simpler surfaces. These simpler surfaces are typically connected along their edges. Attributes include an ID and type, with functionalities to manipulate and query the composite surface structure.
        
        - `id` (str): A unique identifier for the PolySurface.
        - `type` (str): Class name, "PolySurface".
        """
        self.id = generateID()
        self.type = __class__.__name__

    def __id__(self) -> 'str':
        """Returns the unique identifier of the PolySurface object.
        Similar to the NurbsSurface, this method provides the unique ID of the PolySurface, facilitating its identification and tracking across various operations or within data structures that involve multiple surfaces.

        #### Returns:
        `str`: The unique identifier of the PolySurface, prefixed with "id:".

        #### Example usage:
        ```python
        poly_surface = PolySurface()
        print(poly_surface.__id__())
        # Output format: "id:{unique_id}"
        ```
        """
        return f"id:{self.id}"

    def __str__(self) -> 'str':
        """Generates a string representation of the PolySurface object.
        Provides a simple string that identifies the PolySurface, mainly through its class name. This is helpful for debugging, logging, or any scenario where a quick textual representation of the object is beneficial.

        #### Returns:
        `str`: A string representation of the PolySurface object.

        #### Example usage:
        ```python
        poly_surface = PolySurface()
        print(poly_surface)
        # Output: "PolySurface({self})"
        ```
        """
        return f"{__class__.__name__}({self})"
