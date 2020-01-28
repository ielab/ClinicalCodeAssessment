import json
import os

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

EXTENSIONS = set(["csv"])


def removeUploadedFile():
    directory = "data"
    for path in os.listdir(directory):
        p = os.path.join(directory, path)
        if os.path.isfile(p):
            os.remove(p)


def fileFormat(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in EXTENSIONS
