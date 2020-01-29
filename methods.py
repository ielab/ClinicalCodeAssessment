import os


def removeUploadedFile():
    directory = "data"
    for path in os.listdir(directory):
        p = os.path.join(directory, path)
        if os.path.isfile(p):
            os.remove(p)


def getCUIPreferredTerm(cui):
    return cui


def getCUIPreferredTerms(content):
    for item in content:
        print("ID: ", item["ID"])
        print("DIAGNOSIS: ", item["DIAGNOSIS"])
        print("CUI_SET: ", item["CUI_SET"])
        print("-------------------------------------------------------------------------------------------")
    return content
