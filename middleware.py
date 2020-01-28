import csv
import glob
import json
from methods import *


# Load the config file
print("--------------------------------------------------")
print("Loading Config File...")
with open('Config.json') as configFile:
    config = json.load(configFile)
globalConfig = config
umlsPrefix = config["UMLSURLPREFIX"]
WaitressConfig = config["WAITRESS"]
print("Config File Loaded.")
print("--------------------------------------------------")

EXTENSIONS = set(globalConfig["EXTENSIONS"])


def processFile():
    path = globalConfig["UPLOADFOLDER"] + "/*.csv"
    files = glob.glob(path)
    content = []
    with open(files[0], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            temp = {}
            if row[0] != "0":
                temp["ID"] = row[0]
                temp["DIAGNOSIS"] = row[1]
                temp["CUI_SET"] = row[2:]
                content.append(temp)
    res = getCUIConcepts(content)
    return res


def fileFormat(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONS
