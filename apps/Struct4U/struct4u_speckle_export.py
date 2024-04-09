import os
import sys
import subprocess
import requests
import webbrowser
import xml.etree.ElementTree as ET
from datetime import datetime
import specklepy
from specklepy.api.client import SpeckleClient
from specklepy.objects import Base
from specklepy.objects.geometry import Point, Line

from bp_single_file import *
import bp_send_file


def timestamp(rec):
    print(f"[Timestamp] {rec} - {datetime.now()}")
    return datetime.now()


def clear_log_file(log_file_path):
    try:
        with open(log_file_path, 'w') as log_file:
            log_file.truncate(0)
    except Exception as e:
        sys.exit()


def write_to_log(file_path, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(file_path, 'a') as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def open_log():
    try:
        subprocess.Popen(['start', log_filename], shell=True)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def fail_log():
    write_to_log(log_filename, f"Failed to create Speckle model.")


def set_running_flag(ini_file_path, is_running):
    temp_data = {}
    if os.path.exists(ini_file_path):
        with open(ini_file_path, 'r', encoding="utf-8") as config_file:
            for line in config_file:
                line = line.strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                    temp_data[key] = value
    temp_data["running"] = str(is_running).lower()

    with open(ini_file_path, 'w', encoding="utf-8") as config_file:
        for key, value in temp_data.items():
            config_file.write(f"{key}={value}\n")


ini_file_path = os.path.join(os.getenv('LOCALAPPDATA'), 'Struct4u', 'PythonExport.ini')
log_filename = os.path.join(os.getenv('LOCALAPPDATA'), 'Struct4u', "Struct4USpeckleExport.log")
clear_log_file(log_filename)

set_running_flag(ini_file_path, True)

credential_data= {}

if os.path.exists(ini_file_path):
    with open(ini_file_path, 'r', encoding="utf-8") as config_file:
        for j in config_file:
            j = j.replace("\n", "")
            c = j.split("=")
            try:
                credential_data[c[0]] = c[1]
            except:
                pass


def validate_credentials(credential_data):
    if not credential_data["speckle_server"].startswith(("https://", "http://")):
        return False, write_to_log(log_filename, "speckle_server must start with 'https://' or 'http://'")

    if not credential_data["api_token"]:
        return False, write_to_log(log_filename, "api_token must be filled in.")
    try:
        response = requests.get(credential_data["speckle_server"], headers={"Authorization": f"Bearer {credential_data['api_token']}"})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return False, write_to_log(log_filename, f"Failed to connect with api_token to speckle_server: {str(e)}.")

    if "stream_id" not in credential_data:
        write_to_log(log_filename, "stream_id is not found.")

    if "message_commit" not in credential_data:
        write_to_log(log_filename, "message_commit can be empty.")

    if not os.path.exists(credential_data["filepath"]):
        return False, write_to_log(log_filename, "filepath is not a valid path.")
    
    return True, True


if validate_credentials(credential_data)[0] == False:
    fail_log()
    open_log()
    sys.exit()


#load .xml file to buildingpy objects
tree = ET.parse(credential_data['filepath'])
root = tree.getroot()
write_to_log(log_filename, f"Reading {credential_data['filepath']}.")

#convert .xml to buildingpy objects.
obj = []

#LoadGrid and create in Speckle
XYZ = XMLImportNodes(tree)

obj = obj + XMLImportGrids(tree, 1000)
obj.append(XMLImportPlates(tree))

print(obj)
# sys.exit()

#BEAMS
BeamsFrom = root.findall(".//Beams/From_node_number")
BeamsNumber = root.findall(".//Beams/Number")
BeamsTo = root.findall(".//Beams/To_node_number")
BeamsName = root.findall(".//Beams/Profile_number")
BeamsLayer = root.findall(".//Beams/Layer")
BeamsRotation = root.findall(".//Beams/Angle")

#PROFILES
ProfileNumber = root.findall(".//Profiles/Number")
ProfileName = root.findall(".//Profiles/Profile_name")

#BEAMS
for i, j, k, l, m in zip(BeamsFrom, BeamsTo, BeamsName, BeamsNumber, BeamsRotation):
    profile_name = ProfileName[int(k.text)-1].text
    profile_name = profile_name.split()[0]
    if profile_name == None:
        write_to_log(log_filename, f"No profile name '{profile_name}' found.")
    else:
        start = XYZ[1][XYZ[0].index(i.text)]
        end = XYZ[1][XYZ[0].index(j.text)]
        try:
            pf = Frame.by_startpoint_endpoint_profile_name_shapevector(start, end, profile_name, profile_name + "-" + l.text, Vector2(0,0), float(m.text), BaseSteel, None)
            if pf != None:
                obj.append(pf)
        except Exception as e:
            write_to_log(log_filename, f"Could not translate '{profile_name}'.")
write_to_log(log_filename, f"Generated BuildingPy Objects.")

# convert the buildingpy objects to speckle objects
SpeckleObj = bp_send_file.translateObjectsToSpeckleObjects(obj)
write_to_log(log_filename, f"Translated BuildingPy objects to Speckle Objects.")

# convert to speckle objects and return browser link
commit = bp_send_file.TransportToSpeckle(credential_data, SpeckleObj)

if commit[0] == True:
    if commit[2] != None:
        write_to_log(log_filename, f"Created new Speckle Stream, ID: {commit[2]}")
        credential_data["stream_id"] = commit[2]
        credential_data["commit_id"] = commit[3]

        #update the ini file
        with open(ini_file_path, 'w', encoding="utf-8") as config_file:
            for key, value in credential_data.items():
                config_file.write(f"{key}={value}\n")

    write_to_log(log_filename, f"Transported items to Speckle.")

else:
    write_to_log(log_filename, f"{commit[1]}")
    fail_log()
    open_log()

try:
    webbrowser.open(commit[1])
    write_to_log(log_filename, f"Succesfully created Speckle model.")
    
except:
    write_to_log(log_filename, f"Could not open {commit[1]} in browser.")
    fail_log()

set_running_flag(ini_file_path, False)