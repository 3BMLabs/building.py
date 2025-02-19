# [included in GIS2BIM singlefile]
# [!not included in GIS2BIM singlefile - start]

# -*- coding: utf8 -*-
#***************************************************************************
#*   Copyright (c) 2021 Maarten Vroegindeweij <maarten@3bm.co.nl>          *
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

"""This module provides tools to load GIS information from the Netherlands
"""

__title__= "GIS2BIM_NL"
__author__ = "Maarten Vroegindeweij"
__url__ = "https://github.com/DutchSailor/GIS2BIM"

from . import GIS2BIM

import sys
import json
import urllib
import urllib.request
import time
import xml.etree.ElementTree as ET

import requests

# [!not included in GIS2BIM singlefile - end]

#import urllib.request, json

#jsonpath = "$.GIS2BIMserversRequests.webserverRequests[?(@.title==NetherlandsPDOKServerURL)].serverrequestprefix"

## Webserverdata NL
NLPDOKServerURL = GIS2BIM.GetWebServerData('NLPDOKServerURL_28992','webserverRequests','serverrequestprefix')
NLPDOKCadastreCadastralParcels = GIS2BIM.GetWebServerData('NLPDOKCadastreCadastralParcels_28992','webserverRequests','serverrequestprefix') #For curves of Cadastral Parcels
NLPDOKCadastreCadastralParcelsNummeraanduiding = GIS2BIM.GetWebServerData('NLPDOKCadastreCadastralParcelsNummeraanduiding_28992','webserverRequests','serverrequestprefix') #For 'nummeraanduidingreeks' of Cadastral Parcels
NLPDOKCadastreOpenbareruimtenaam = GIS2BIM.GetWebServerData('NLPDOKCadastreOpenbareruimtenaam_28992','webserverRequests','serverrequestprefix')#For 'openbareruimtenaam' of Cadastral Parcels
NLPDOKBAGBuildingCountour = GIS2BIM.GetWebServerData('NLPDOKBAGBuildingCountour_28992','webserverRequests','serverrequestprefix')  #Building Contour of BAG
NLTUDelftBAG3DV1 = GIS2BIM.GetWebServerData('NLTUDelftBAG3DV1_28992','webserverRequests','serverrequestprefix')  #3D Buildings of BAG
NLRuimtelijkeplannenBouwvlak = GIS2BIM.GetWebServerData('NLRuimtelijkeplannenBouwvlak_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2016 = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_2016_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2017 = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_2017_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2018 = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_2018_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2019 = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_2019_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2020 = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_2020_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfoto2021 = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_2021_28992','webserverRequests','serverrequestprefix')
NLPDOKLuchtfotoActueel = GIS2BIM.GetWebServerData('NL_PDOK_Luchtfoto_actueel_28992','webserverRequests','serverrequestprefix')
NLRuimtelijkeplannenEnkelbestemming = GIS2BIM.GetWebServerData('NLRuimtelijkeplannenEnkelbestemming_28992','webserverRequests','serverrequestprefix')
NLNatura2000 = GIS2BIM.GetWebServerData('NL_PDOK_natura2000_28992','webserverRequests','serverrequestprefix')
NLGeluidskaartAlleBronnen = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_alle_bronnen_28992','webserverRequests','serverrequestprefix')
NLRIVMGeluidskaartldenwegverkeer = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_lden_wegverkeer_28992','webserverRequests','serverrequestprefix')
NLRIVMGeluidskaartldenspoor = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_lden_spoor_28992','webserverRequests','serverrequestprefix')
NLRisicocontourbasisnet = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_lden_spoor_28992','webserverRequests','serverrequestprefix')
NLRisicocontourEV = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_lden_spoor_28992','webserverRequests','serverrequestprefix')
NLRisicocontourEVbrand = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_lden_spoor_28992','webserverRequests','serverrequestprefix')
NLRisicocontourEVexplosie = GIS2BIM.GetWebServerData('NL_RIVM_Geluidskaart_lden_spoor_28992','webserverRequests','serverrequestprefix')


NLTUDelftBAG3D = GIS2BIM.GetWebServerData('NLTUDelftBAG3D_28992','webserverRequests','serverrequestprefix')

NLTUDelftBAG3DDownloadPrefix = GIS2BIM.GetWebServerData('NLTUDelftBAG3Ddownload_28992','webserverRequests','serverrequestprefix')

NLPDOKBGTURL1 = "https://api.pdok.nl/lv/bgt/download/v1_0/full/custom"
NLPDOKBGTURL2 = "https://api.pdok.nl"

## Xpath for several Web Feature Servers
NLPDOKxPathOpenGISposList = GIS2BIM.GetWebServerData('NLPDOKxPathOpenGISposList','Querystrings','querystring')
NLPDOKxPathOpenGISPos = GIS2BIM.GetWebServerData('NLPDOKxPathOpenGISPos','Querystrings','querystring')
NLPDOKxPathStringsCadastreTextAngle = GIS2BIM.GetWebServerData('NLPDOKxPathStringsCadastreTextAngle','Querystrings','querystring')
NLPDOKxPathStringsCadastreTextValue = GIS2BIM.GetWebServerData('NLPDOKxPathStringsCadastreTextValue','Querystrings','querystring')
NLPDOKxPathOpenGISPosList2 = GIS2BIM.GetWebServerData('NLPDOKxPathOpenGISPosList2','Querystrings','querystring')
NLTUDelftxPathString3DBagGround = GIS2BIM.GetWebServerData('NLTUDelftxPathString3DBagGround','Querystrings','querystring')
NLTUDelftxPathString3DBagRoof = GIS2BIM.GetWebServerData('NLTUDelftxPathString3DBagRoof','Querystrings','querystring')

NLTUDelftxPathString3DBagTileId = GIS2BIM.GetWebServerData('NLTUDelftxPathString3DBagTileId','Querystrings','querystring')
NLTUDelftxPathString3DBag2 = GIS2BIM.GetWebServerData('NLTUDelftxPathString3DBag2','Querystrings','querystring')

NLPDOKKadasterBasisvoorziening3DCityJSONVolledig = GIS2BIM.GetWebServerData("NLPDOKKadasterBasisvoorziening3DCityJSONVolledig","webserverRequests","serverrequestprefix")

xPathStrings3DBag = [NLTUDelftxPathString3DBagGround, NLTUDelftxPathString3DBagRoof]
xPathStrings3DBAG2 = [NLTUDelftxPathString3DBagTileId, NLPDOKxPathOpenGISposList, NLTUDelftxPathString3DBag2]
xPathStringsCadastreTextAngle = [NLPDOKxPathStringsCadastreTextAngle, NLPDOKxPathStringsCadastreTextValue]

#Country specific

#NL Netherlands
def NL_GetLocationData(PDOKServer, City, Streetname, Housenumber):
# Use PDOK location server to get X & Y data
	SN = Streetname.replace(" ", "%20")
	requestURL =  PDOKServer + City +"%20and%20" + SN + "%20and%20" + Housenumber
	urlFile = urllib.request.urlopen(requestURL)
	jsonList = json.load(urlFile)
	jsonList = jsonList["response"]["docs"]
	jsonList1 = jsonList[0]
	RD = jsonList1['centroide_rd']
	RD = RD.replace("("," ").replace(")"," ")
	RD = RD.split()
	RDx = float(RD[1])
	RDy = float(RD[2])
	result = [RDx,RDy,requestURL]
	
	return result

def bgtDownloadURL(X,Y,bboxWidth,bboxHeight,timeout):
	polygonString = GIS2BIM.CreateBoundingBoxPolygon(X,Y,bboxWidth,bboxHeight,2)
	
	url = NLPDOKBGTURL1
	url2 = NLPDOKBGTURL2

	##Define data 
	qryPart1 = '{"featuretypes":['
	qryPart2 = '"bak","begroeidterreindeel","bord","buurt","functioneelgebied","gebouwinstallatie","installatie","kast","kunstwerkdeel","mast","onbegroeidterreindeel","ondersteunendwaterdeel","ondersteunendwegdeel","ongeclassificeerdobject","openbareruimte","openbareruimtelabel","overbruggingsdeel","overigbouwwerk","overigescheiding","paal","pand","put","scheiding","sensor","spoor","stadsdeel","straatmeubilair","tunneldeel","vegetatieobject","waterdeel","waterinrichtingselement","waterschap","weginrichtingselement","wijk","wegdeel"'
	qryPart3 = '],"format":"gmllight","geofilter":"POLYGON('
	qryPart4 = polygonString
	qryPart5 = ')"}'
	
	data = qryPart1 +  qryPart2 + qryPart3 + qryPart4 + qryPart5
	dataquery = data
	
	headers = requests.structures.CaseInsensitiveDict()
	headers["accept"] = "application/json"
	headers["Content-Type"] = "application/json"
	
	resp = requests.post(url, headers=headers, data=data)
	
	jsondata = json.loads(resp.text)
	data = jsondata["downloadRequestId"]
	urlstatus = url + "/" + data + "/status" 
	
	# Check URL Status
	
	req = urllib.request.urlopen(urlstatus)
	req2 = req.read().decode('utf-8')
	progressStatus = int(json.loads(req2)['progress'])
	
	timer = 0
	
	while timer < timeout:
	    req = urllib.request.urlopen(urlstatus)
	    req2 = req.read().decode('utf-8')    
	    progressStatus = int(json.loads(req2)['progress'])
	    status = json.loads(req2)['status']
	    if status == "COMPLETED":
	        try:
	            downloadURL = url2 + json.loads(req2)["_links"]["download"]["href"]
	        except:   
	            downloadURL = "unable to get downloadlink"        
	        message = status
	        break
	    elif timer > timeout:
	        downloadURL = "empty"
	        message = "timeout"
	        break
	    else: 
	        time.sleep(1)
	    timer = timer + 1
	return downloadURL

def BAG3DDownload(bboxString, tempFolder):
	#Download 3D BAG as CityJSON
	import requests
	url = NLTUDelftBAG3D
	xPathString1 = xPathStrings3DBAG2[0]

	# Webrequest to obtain tilenumbers based on bbox
	urlreq = url + bboxString
	response = requests.get(urlreq)
	tree = ET.fromstring(response.text)
	res = tree.findall(xPathString1)
	for i in res:
		tile_id = i.text
		tile_id2 = tile_id.replace("/","-")
		url = NLTUDelftBAG3DDownloadPrefix + tile_id + "/" + tile_id2 + ".city.json"
		path = tempFolder + tile_id2 + ".city.json"
		r = requests.get(url)
		with open(path, 'wb') as f:
			f.write(r.content)
	return res

class NL_Geocoding:
    def __init__(self):
        
        self.servername = NLPDOKServerURL
        self.bron = None
        self.woonplaatscode = None
        self.type = None
        self.woonplaatsnaam = None
        self.wijkcode = None
        self.huis_nlt = None
        self.openbareruimtetype = None
        self.buurtnaam = None
        self.gemeentecode = None
        self.rdf_seealso =  None
        self.rdf_seealso =  None
        self.weergavenaam =  None
        self.straatnaam_verkort =  None
        self.id =  None
        self.gekoppeld_perceel =  None
        self.gemeentenaam =  None
        self.buurtcode =  None
        self.wijknaam =  None
        self.identificatie =  None
        self.openbareruimte_id =  None
        self.waterschapsnaam =  None
        self.provinciecode =  None
        self.postcode =  None
        self.provincienaam =  None
        self.centroide_ll =  None
        self.centroid_X = None
        self.centroid_Y = None
        self.nummeraanduiding_id =  None
        self.waterschapscode =  None
        self.adresseerbaarobject_id =  None
        self.huisnummer =  None
        self.provincieafkorting =  None
        self.centroide_rd =  None
        self.rdx = None
        self.rdy = None
        self.straatnaam =  None
        self.score =  None
        self.url = None

    def by_address(self, City: str, Streetname: str, Housenumber: str):
        # Use PDOK location server to get X & Y data
        PDOKServer = self.servername
        SN = Streetname.replace(" ", "%20")
        self.url = PDOKServer + City + "%20and%20" + SN + "%20and%20" + Housenumber
        urlFile = urllib.request.urlopen(self.url)
        jsonList = json.load(urlFile)
        jsonList = jsonList["response"]["docs"]
        jsonList1 = jsonList[0]
        self.fill_param(jsonList1)
        return self

    def by_rdx_rdy(self, rdx: float, rdy: float):
        PDOKServer = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse?X=RDX&Y=RDY&rows=1"
        PDOKServer = PDOKServer.replace("RDX", str(rdx))
        PDOKServer = PDOKServer.replace("RDY", str(rdy))
        urlFile = urllib.request.urlopen(PDOKServer)
        jsonList = json.load(urlFile)
        id = jsonList["response"]["docs"][0]["id"]
        PDOKServer = self.servername
        PDOKServer = PDOKServer + id
        urlFile = urllib.request.urlopen(PDOKServer)
        jsonList = json.load(urlFile)
        jsonList = jsonList["response"]["docs"]
        jsonList1 = jsonList[0]
        self.fill_param(jsonList1)
        self.url = PDOKServer
        return self
    def fill_param(self, resp):
        jsonList1 = resp
        RD = jsonList1['centroide_rd']
        RD = RD.replace("(", " ").replace(")", " ")
        RD = RD.split()
        RDx = float(RD[1])
        RDy = float(RD[2])
        LatLon = jsonList1['centroide_ll']
        LatLon = LatLon.replace("(", " ").replace(")", " ")
        LatLon = LatLon.split()
        Lat = float(LatLon[1])
        Lon = float(LatLon[2])
        self.bron = jsonList1['bron']
        self.woonplaatscode = jsonList1['woonplaatscode']
        self.type = jsonList1['type']
        self.woonplaatsnaam = jsonList1['woonplaatsnaam']
        self.wijkcode = jsonList1['wijkcode']
        self.huis_nlt = jsonList1['huis_nlt']
        self.openbareruimtetype = jsonList1['openbareruimtetype']
        self.buurtnaam = jsonList1['buurtnaam']
        self.gemeentecode = jsonList1['gemeentecode']
        self.rdf_seealso =  jsonList1['rdf_seealso']
        self.weergavenaam =  jsonList1['weergavenaam']
        self.straatnaam_verkort =  jsonList1['straatnaam_verkort']
        self.id =  jsonList1['id']
        self.gekoppeld_perceel =  jsonList1['gekoppeld_perceel']
        self.gemeentenaam =  jsonList1['gemeentenaam']
        self.buurtcode =  jsonList1['buurtcode']
        self.wijknaam =  jsonList1['wijknaam']
        self.identificatie =  jsonList1['identificatie']
        self.openbareruimte_id =  jsonList1['openbareruimte_id']
        self.waterschapsnaam =  jsonList1['waterschapsnaam']
        self.provinciecode =  jsonList1['provinciecode']
        self.postcode =  jsonList1['postcode']
        self.provincienaam =  jsonList1['provincienaam']
        self.centroide_ll =  jsonList1['centroide_ll']
        self.lat = Lat
        self.lon = Lon
        self.nummeraanduiding_id =  jsonList1['nummeraanduiding_id']
        self.waterschapscode =  jsonList1['waterschapscode']
        self.adresseerbaarobject_id =  jsonList1['adresseerbaarobject_id']
        self.huisnummer =  jsonList1['huisnummer']
        self.provincieafkorting =  jsonList1['provincieafkorting']
        self.centroide_rd =  jsonList1['centroide_rd']
        self.rdx = RDx
        self.rdy = RDy
        self.straatnaam =  jsonList1['straatnaam']
        self.score =  jsonList1['score']
        return self
