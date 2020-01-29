import csv
import glob
import json
import shutil
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
    res = getCUIPreferredTerms(content)
    return res


def fileFormat(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONS


def reset():
    folder = globalConfig["UPLOADFOLDER"] + "/"
    for filename in os.listdir(folder):
        filePath = os.path.join(folder, filename)
        filePart = filename.split(".")
        fileType = filePart[len(filePart) - 1]
        if fileType != "template" and fileType != "tpl":
            try:
                if os.path.isfile(filePath) or os.path.islink(filePath):
                    os.unlink(filePath)
                elif os.path.isdir(filePath):
                    shutil.rmtree(filePath)
            except Exception as err:
                print("Failed To Remove %s. Error: %s" % (filePath, err))