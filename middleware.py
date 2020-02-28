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
WaitressConfig = config["WAITRESS"]
ESConfig = config["ES"]
progressConfig = config["PROGRESSES"]
print("Config File Loaded.")
print("--------------------------------------------------")


def processFile():
    csvPath = globalConfig["DATAFOLDER"] + "/*.csv"
    CSVPath = globalConfig["DATAFOLDER"] + "/*.CSV"
    csvFiles = glob.glob(csvPath)
    CSVFiles = glob.glob(CSVPath)
    files = csvFiles + CSVFiles
    content = []
    with open(files[0], "r") as file:
        reader = csv.reader(file)
        unique_id = 1
        for row in reader:
            temp = {"ID": unique_id, "DIAGNOSIS": row[0], "CUI_SET": row[1:]}
            content.append(temp)
            unique_id += 1
    res = getCUIPreferredTerms(content, ESConfig)
    return res


def getUserProgress(user, uid):
    res = getProgress(user, uid, progressConfig)
    return res


def createUserProgress(data):
    res = createProgress(data, progressConfig)
    return res


def updateUserProgress(uid, data):
    res = updateProgress(uid, data, progressConfig)
    return res


def getUserId(user):
    userID = getUserUniqueID(user, progressConfig)
    if userID is None:
        res = {
            "user_id": None
        }
    else:
        res = {
            "user_id": userID
        }
    return res
