from packages.GIS2BIM.GIS2BIM_NL import *
from packages.GIS2BIM.GIS2BIM import *
from project.fileformat import *
from exchange.GIS2BIM import *
from geometry.mesh import Mesh
from library.material import *
from exchange.image_to_mesh import *

# Description
# This script creates lines for the BGT

# SETTINGS
GISProject = BuildingPy("BGT Test")
GISProject.closed = False
GISProject.autoclose = False

tempfolder = "C:/TEMP/GIS/"
lst = NL_GetLocationData(NLPDOKServerURL, "Dordrecht", "werf van schouten", "501")
Bboxwidth = 700  # Meter

# BASE VALUES
RdX = lst[0]
RdY = lst[1]
Bbox = GIS2BIM.CreateBoundingBox(RdX, RdY, Bboxwidth, Bboxwidth, 0)

xpath1 = './/{http://www.opengis.net/gml}featureMember'
xpath2 = './/{http://www.opengis.net/gml}pos'
xpath3 = './/{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}openbareRuimteNaam.tekst'
xpath4 = './/{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}openbareRuimteNaam.positie_1.hoek'
xpath5 = './/{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}VegetatieObject.plus-type'

def CurvesFromGML(tree, xPathString, dx, dy, BoxWidth, BoxHeight, scale):
	bbx = -dx
	bby = -dy

	# Bounding box definition
	bounding_box = [bbx, bby, BoxWidth, BoxHeight]
	min_x = bounding_box[0] - (bounding_box[2] / 2)
	min_y = bounding_box[1] - (bounding_box[3] / 2)
	max_x = bounding_box[0] + (bounding_box[2] / 2)
	max_y = bounding_box[1] + (bounding_box[3] / 2)

	# get data from xml
	root = tree.getroot()

	# for loop to get each element in an array
	XMLelements = []
	for elem in root.iter():
		XMLelements.append(elem)

	xpathfound = root.findall(xPathString)

	# for loop to get all polygons in an array
	BPCurves = []
	for x in xpathfound:
		if x.text:
			try:
				newPolygon = x.text.split(" ")
				polygon_is_inside_bounding_box = False
				x = 0
				xyPolygon = []
				for i in range(0, int(len(newPolygon) / 2)):
					xy_coord = [newPolygon[x], newPolygon[x + 1]]
					xy_coord_trans = [round((float(newPolygon[x]) - bbx) * scale),
									  round((float(newPolygon[x + 1]) - bby) * scale)]
					xyPolygon.append(xy_coord_trans)
					x += 2
					if checkIfCoordIsInsideBoundingBox(xy_coord, min_x, min_y, max_x, max_y):
						polygon_is_inside_bounding_box = True
				if polygon_is_inside_bounding_box:
					# xyPolygons.append(xyPolygon)
					pointlist = []
					for j in xyPolygon:
						pointlist.append(Point(j[0], j[1], 0))
					PC = PolyCurve().by_points(pointlist)
					#a.MakeFace = Face
					#a.ViewObject.DrawStyle = DrawStyle
					#a.ViewObject.LineColor = LineColor
					#a.ViewObject.ShapeColor = ShapeColor
					BPCurves.append(PC)
			except:
				BPCurves.append("_none_")
		else:
			BPCurves.append("_none_")
	return BPCurves

# BGT FOLDERS
folderBGT = tempfolder + "BGT/"

xpath = './/{http://www.opengis.net/gml}posList'

bgt_curves_faces_color = [(223,230,208),
(223,230,208),
(205,230,237),
(226,226,226),
(234,234,234),
(220,155,140),
(220,155,140),
(205,230,237),
(234,234,234)]

bgt_curves_lines = ["bgt_functioneelgebied",
"bgt_gebouwinstallatie",
"bgt_kunstwerkdeel",
"bgt_overbruggingsdeel",
"bgt_overigbouwwerk",
"bgt_overigescheiding",
"bgt_scheiding",
"bgt_spoor",
"bgt_tunneldeel"]

bgt_curves_faces = ["bgt_begroeidterreindeel",
"bgt_onbegroeidterreindeel",
"bgt_ondersteunendwaterdeel",
"bgt_ondersteunendwegdeel",
"bgt_overbruggingsdeel",
"bgt_overigbouwwerk",
"bgt_pand",
"bgt_waterdeel",
"bgt_wegdeel"]

bgt_curves_faces_color = [(223,230,208),
(223,230,208),
(205,230,237),
(226,226,226),
(234,234,234),
(220,155,140),
(220,155,140),
(205,230,237),
(234,234,234)]

def BoomFromGML(filePath,dx,dy,BoxWidth, BoxHeight,scale, DecimalNumbers):
	# group X and Y Coordinates
	bbx = -dx
	bby = -dy

	# Bounding box definition
	bounding_box = [bbx, bby, BoxWidth, BoxHeight]
	min_x = bounding_box[0] - (bounding_box[2] / 2)
	min_y = bounding_box[1] - (bounding_box[3] / 2)
	max_x = bounding_box[0] + (bounding_box[2] / 2)
	max_y = bounding_box[1] + (bounding_box[3] / 2)

	xpathpnt = './/{http://www.opengis.net/gml}pos'
	xpathname = './/{http://www.geostandaarden.nl/imgeo/2.1/simple/gml31}plus-type'
	tree = ET.parse(filePath)
	# group X and Y Coordinates of polylines
	posLists = tree.findall(xpathpnt)
	typeLists = tree.findall(xpathname)
	xyPosList = []
	for posList, type in zip(posLists,typeLists):
		dataPosList = posList.text
		typename = type.text
		if typename == 'boom':
			coordSplit = dataPosList.split()
			try:
				if float(coordSplit[2]) == 0:
					XYZCountDimensions = 3
				else:
					XYZCountDimensions = 2
			except:
				XYZCountDimensions = 2
			x = 0
			coordSplitXY = []
			for j in range(0, int(len(coordSplit) / XYZCountDimensions)):
				xy_coord = (round((float(coordSplit[x]) + dx) * scale, DecimalNumbers),
							round((float(coordSplit[x + 1]) + dy) * scale, DecimalNumbers))
				coordSplitXY.append(xy_coord)
				x += XYZCountDimensions

			if checkIfCoordIsInsideBoundingBox(coordSplit, min_x, min_y, max_x, max_y):
				#print(checkIfCoordIsInsideBoundingBox)
				xyPosList.append(coordSplitXY)
			else:
				pass
		else:
			pass

	return xyPosList

path_vegatatieobject = folderBGT + '/bgt_vegetatieobject.gml'

pnts = BoomFromGML(path_vegatatieobject,-RdX,-RdY,Bboxwidth,Bboxwidth,1000,2)

radius = 1500

for i in pnts:

	x = i[0][0]
	y = i[0][1]
	treePart1 = Arc(Point(-radius+x, y, 0), Point(x, radius+y, 0), Point(-radius+x, 50+y, 0))
	GISProject.objects.append(treePart1)
	GISProject.objects.append(Point(x,y,0))


GISProject.to_speckle("cfcafde1df", "GIS2BIM BGT test")

sys.exit()



#Draw bgt_curves_lines
for i in bgt_curves_lines:
	path = folderBGT + '/' + i + '.gml'
	tree = ET.parse(path)
	Curves = CurvesFromGML(tree,xpath,-RdX,-RdY,Bboxwidth,Bboxwidth,1000)
	for j in Curves:
		GISProject.objects.append(j)

#Draw bgt_curves_faces
for i in bgt_curves_faces:
	path = folderBGT + '/' + i + '.gml'
	tree = ET.parse(path)
	Curves = CurvesFromGML(tree,xpath,-RdX,-RdY,Bboxwidth,Bboxwidth,1000)
	for j in Curves:
		#m = MeshPB().by_polycurve(j, i, BaseBuilding)
		GISProject.objects.append(j)

