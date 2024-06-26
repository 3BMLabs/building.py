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


"""This module provides tools for intervales
"""

__title__ = "interval"
__author__ = "Maarten & Jonathan"
__url__ = "./abstract/interval.py"

import sys
from pathlib import Path
from typing import Any, List

sys.path.append(str(Path(__file__).resolve().parents[1]))

from geometry.point import Point as pnt
from abstract.vector import *

# [!not included in BP singlefile - end]


class Interval:
    """The `Interval` class is designed to represent a mathematical interval, providing a start and end value along with functionalities to handle intervals more comprehensively in various applications."""
    def __init__(self, start: float, end: float):
        """Initializes a new Interval instance.
        
        - `start` (float): The starting value of the interval.
        - `end` (float): The ending value of the interval.
        - `interval` (list, optional): A list that may represent subdivided intervals or specific points within the start and end bounds, depending on the context or method of subdivision.

        """
        self.start = start
        self.end = end
        self.interval = None

    def serialize(self) -> dict:
        """Serializes the interval's attributes into a dictionary.

        This method facilitates converting the interval's properties into a format that can be easily stored or transmitted.

        #### Returns:
            dict: A dictionary containing the serialized attributes of the interval.
        
        #### Example usage:
    	```python

        ```
        """

        return {
            'start': self.start,
            'end': self.end,
            'interval': self.interval
        }

    @staticmethod
    def deserialize(data: dict) -> 'Interval':
        """Reconstructs an Interval object from serialized data contained in a dictionary.

        #### Parameters:
            data (dict): The dictionary containing serialized data of an Interval object.

        #### Returns:
            Interval: A new Interval object initialized with the data from the dictionary.
        
        #### Example usage:
    	```python

        ```
        """

        start = data.get('start')
        end = data.get('end')
        interval = Interval(start, end)
        interval.interval = data.get('interval')
        return interval

    @classmethod
    def by_start_end_count(self, start: float, end: float, count: int) -> 'Interval':
        """Generates a list of equidistant points within the interval.

        This method divides the interval between the start and end values into (count - 1) segments, returning an Interval object containing these points.

        #### Parameters:
            start (float): The starting value of the interval.
            end (float): The ending value of the interval.
            count (int): The total number of points to generate, including the start and end values.

        #### Returns:
            Interval: An Interval instance with its `interval` attribute populated with the generated points.
        
        #### Example usage:
    	```python

        ```
        """
        intval = []
        numb = start
        delta = end-start
        for i in range(count):
            intval.append(numb)
            numb = numb + (delta / (count - 1))
        self.interval = intval
        return self

    def __str__(self) -> str:
        """Generates a string representation of the Interval.

        #### Returns:
            str: A string representation of the Interval, primarily indicating its class name.
        
        #### Example usage:
    	```python

        ```
        """
        return f"{__class__.__name__}"
