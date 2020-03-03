import csv
import glob
import json
import datetime
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
dataConfig = config["DATA"]
print("Config File Loaded.")
print("--------------------------------------------------")


def processFile():
    csvPath = globalConfig["DATAFOLDER"] + "/*.csv"
    CSVPath = globalConfig["DATAFOLDER"] + "/*.CSV"
    txtPath = globalConfig["DATAFOLDER"] + "/*.txt"
    csvFiles = glob.glob(csvPath)
    CSVFiles = glob.glob(CSVPath)
    txtFiles = glob.glob(txtPath)
    files = csvFiles + CSVFiles
    content = []
    if len(txtFiles) > 0:
        with open(txtFiles[0], "r") as file:
            fileContent = file.readlines()
        fileContent = [x.strip() for x in fileContent]
        for line in fileContent:
            splitedLine = line.split(',')
            temp = {"DIAGNOSIS": splitedLine[0], "CUI_SET": splitedLine[1:]}
            content.append(temp)
        res = getCUIPreferredTerms(content, ESConfig)
        return res
    else:
        with open(files[0], "r") as file:
            reader = csv.reader(file)
            for row in reader:
                temp = {"DIAGNOSIS": row[0], "CUI_SET": row[1:]}
                content.append(temp)
        res = getCUIPreferredTerms(content, ESConfig)
        return res


def updateContent():
    newContent = processFile()
    f = open("update_log", "a+")
    f.write(str(datetime.datetime.now()) + "  Updating File...\n")
    f.close()
    print(str(datetime.datetime.now()) + "  Updating File...")
    exists = checkContentExistence(dataConfig)
    if exists is not None:
        oriContent = json.loads(exists)
        updateContentInES(dataConfig, newContent, oriContent)
    else:
        addContent(dataConfig, newContent)


def getUserProgress(user, uid):
    res = getProgress(user, uid, progressConfig, dataConfig)
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


def getContent():
    res = getFileContent(dataConfig)
    return res
