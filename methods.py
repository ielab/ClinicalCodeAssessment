import os
import requests


def removeUploadedFile():
    directory = "data"
    for path in os.listdir(directory):
        p = os.path.join(directory, path)
        if os.path.isfile(p):
            os.remove(p)


def getOneCUIInfo(item, ES):
    url = ES["URL"]
    username = ES["USERNAME"]
    secret = ES["SECRET"]
    should = []
    for c in item:
        temp = {
            "match": {
                "cui": c
            }
        }
        should.append(temp)
    data = {
        "query": {
            "bool": {
                "should": should
            }
        }
    }
    header = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=None, json=data, headers=header, auth=(username, secret))
    cleanedContent = cleanData(response, ES)
    return cleanedContent


def cleanData(response, ES):
    content = response.json()["hits"]["hits"]
    res = []
    for item in content:
        temp = {
            "id": item["_id"],
            "thesaurus": item["_source"]["thesaurus"]
        }
        res.append(temp)
    pref = getPrefTerm(res, ES)
    return pref


def getPrefTerm(data, ES):
    res = []
    for item in data:
        prefTerm = []
        for t in item["thesaurus"]:
            if t["MRCONSO_ISPREF"] == "Y" and t["MRCONSO_LAT"] == "ENG" and t["MRCONSO_STT"] == "PF" and t["MRCONSO_TS"] == "P":
                prefTerm.append(t["MRCONSO_STR"])
        prefTerm = list(dict.fromkeys(prefTerm))
        temp = {
            "cui": item["id"],
            "pref_term": prefTerm[0],
            "url": ES["UMLSURLPREFIX"] + item["id"],
            "rel": None,
        }
        res.append(temp)
    return res


def getCUIPreferredTerms(content, ES):
    res = []
    for item in content:
        cui = getOneCUIInfo(item["CUI_SET"], ES)
        temp = {
            "id": item["ID"],
            "diagnosis": item["DIAGNOSIS"],
            "cuis": cui
        }
        res.append(temp)
    return res
