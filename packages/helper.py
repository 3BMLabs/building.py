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

class generateID:
    def __init__(self) -> None:
        self.id = None
        self.object = None
        self.name = None
        self.generateID()

    def generateID(self) -> None:
        id = ""
        lengthID = 12
        random_source = string.ascii_uppercase + string.digits
        for x in range(lengthID):
            id += random.choice(random_source)

        id_list = list(id)
        self.id = f"#"+"".join(id_list)
        return f"test {self.__class__.__name__}"

    def __repr__(self) -> str:
        return f"{self.id}"


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

def is_null(lst):
    return all(el is None for el in lst)

def clean_list(input_list, preserve_indices=True):
    if not input_list:
        return input_list
    
    culled_list = []

    if preserve_indices:
        if is_null(input_list):
            return None
        
        j = len(input_list) - 1
        while j >= 0 and input_list[j] is None:
            j -= 1

        for i in range(j + 1):
            sublist = input_list[i]

            if isinstance(sublist, list):
                val = clean_list(sublist, preserve_indices)
                culled_list.append(val)
            else:
                culled_list.append(input_list[i])
    else:
        if is_null(input_list):
            return []
        
        for el in input_list:
            if isinstance(el, list):
                if not is_null(el):
                    val = clean_list(el, preserve_indices=False)
                    if val:
                        culled_list.append(val)
            elif el is not None:
                culled_list.append(el)
            
    return culled_list

def flatten(lst):
    flat_list = []
    for sublist in lst:
        try:
            for item in sublist:
                flat_list.append(item)
        except:
            flat_list.append(sublist)
    return flat_list

def all_true(lst):
    for element in lst:
        if not element:
            return False
    return True