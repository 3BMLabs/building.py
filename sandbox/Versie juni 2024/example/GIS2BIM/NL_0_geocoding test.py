from packages.GIS2BIM.GIS2BIM_NL import *

test = NL_GetLocationData(NLPDOKServerURL,"Dordrecht","werf van schouten", "501")

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

geoc = NL_Geocoding().by_address("Dordrecht","werf van schouten", "501")
geoc2 = NL_Geocoding().by_rdx_rdy(194195.304, 465885.902)

#print(geoc.rdx)
#print(geoc2.url)
