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


"""This module provides import data from SVG file
"""

__title__= "SVG"
__author__ = "Maarten & Jonathan"
__url__ = "./exchange/svg.py"


#reader
#drawsection -> convert point list to polyline (like text)
#CONVERT TEXT .SVG TO .JSON FILE
# import xml.etree.ElementTree as ET
# import json, os, glob

# def write_glyphs_to_json(svg_file, json_file):
# 	try:
# 	    tree = ET.parse(svg_file)
# 	    root = tree.getroot()

# 	    glyphs = {}

# 	    for glyph in root.findall(".//{http://www.w3.org/2000/svg}glyph"):
# 	        try:
# 	            unicode_name = glyph.attrib['unicode']
# 	            glyph_name = glyph.attrib['glyph-name']
# 	            path_d = glyph.attrib['d']
# 	            glyphs[unicode_name] = {
# 	                'glyph-name': glyph_name,
# 	                'glyph-path': path_d
# 	            }
# 	        except:
# 	            pass

# 	    with open(json_file, 'w') as f:
# 	    	json.dump(glyphs, f, indent=4)
# 	except:
# 		pass


#do this for whole folder (if nan exist)

# folder_svgpath = "font_svg"
# folder_jsonpath = "font_json"
# file_paths = glob.glob(os.path.join(folder_svgpath, "*"))
# for x in file_paths:
# 	svg_file = f"{x}"
# 	json_file = folder_jsonpath + "/" + x.split(f"{folder_svgpath}\\")[1].replace(".svg", "") + ".json"
# 	write_glyphs_to_json(svg_file, json_file)