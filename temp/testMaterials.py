import json


def rgb_to_int(rgb):
    r, g, b = [max(0, min(255, c)) for c in rgb]

    return (255 << 24) | (r << 16) | (g << 8) | b

jsonFile = "C:/Users/mikev/Documents/GitHub/building.py/library/material.json"

jsonFileStr = open(jsonFile, "r").read()

with open(jsonFile) as f:
    data = json.load(f)

print(data)

class searchMaterial:
    def __init__(self, name):
        self.name = name
        self.color = []
        self.synonyms = None
        for item in data:
            for i in item.values():
                synonymList = i[0]["synonyms"]
                if self.name in synonymList:
                    self.color = i[0]["color"]

test = searchMaterial("Beton").color   #kleur van beton
