import requests


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
            "unchecked": len(cui),
            "cuis": cui
        }
        res.append(temp)
    return res


def getProgress(user, uid, progressConfig):
    header = {
        "Content-Type": "application/json"
    }
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "user": user
                        },
                        "match": {
                            "_id": uid
                        }
                    }
                ]
            }
        }
    }
    url = progressConfig["URL"] + progressConfig["INDEX"] + "_search?pretty"
    response = requests.post(url, data=None, json=query, headers=header)
    res = response.json()
    return res


def createProgress(data, progressConfig):
    header = {
        "Content-Type": "application/json"
    }
    url = progressConfig["URL"] + progressConfig["INDEX"] + "_doc/?refresh=true"
    response = requests.post(url, data=None, json=data, headers=header)
    res = response.json()
    return res


def updateProgress(uid, data, progressConfig):
    header = {
        "Content-Type": "application/json"
    }
    url = progressConfig["URL"] + progressConfig["INDEX"] + "_doc/" + uid + "?refresh=true"
    response = requests.post(url, data=None, json=data, headers=header)
    res = response.json()
    return res


def getUserUniqueID(user, progressConfig):
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "match": {
                            "user": user
                        }
                    }
                ]
            }
        }
    }
    header = {
        "Content-Type": "application/json"
    }
    url = progressConfig["URL"] + progressConfig["INDEX"] + "_search?pretty"
    response = requests.post(url, data=None, json=query, headers=header)
    content = response.json()
    hit = content["hits"]["total"]["value"]
    if hit > 0:
        userId = content["hits"]["hits"][0]["_id"]
    else:
        userId = None
    return userId
