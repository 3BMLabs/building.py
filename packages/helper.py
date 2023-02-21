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


"""This module provides a module with helper utils
"""

__title__= "shape"
__author__ = "Maarten & Jonathan"
__url__ = "./package/helper.py"


import string, random, json

def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list))
    raise ValueError("'{char}' is not in list".format(char=char))

def generateID():
    id = ""
    prefixID = "#"
    lengthID = 12
    random_source = string.ascii_uppercase + string.digits

    for x in range(lengthID):
        id += random.choice(random_source)

    id_list = list(id)
    id = "".join(id_list)
    return f"{prefixID}{id}"

def findjson(id, json_string):
    #faster way to search in json
    results = []

    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json.loads(json_string, object_hook=_decode_dict) # Return value ignored.
    return results

def list_transpose(lst):
    #list of lists, transpose columns/rows
    newlist = list(map(list, zip(*lst)))
    return newlist