import requests
import json
import datetime


def getResponse(Config, url, data=None, header=None, method=None):
    if method == "post":
        if Config["USERNAME"] != "":
            username = Config["USERNAME"]
            secret = Config["SECRET"]
            response = requests.post(url, data=None, json=data, headers=header, auth=(username, secret))
        else:
            response = requests.post(url, data=None, json=data, headers=header)
        return response
    elif method == "get":
        if Config["USERNAME"] != "":
            username = Config["USERNAME"]
            secret = Config["SECRET"]
            response = requests.get(url, auth=(username, secret))
        else:
            response = requests.get(url)
        return response


def getOneCUIInfo(item, ES):
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
    response = getResponse(ES, ES["URL"], data, header, "post")
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
            if t["MRCONSO_ISPREF"] == "Y" and t["MRCONSO_LAT"] == "ENG" and t["MRCONSO_STT"] == "PF" and t[
                "MRCONSO_TS"] == "P":
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
            "diagnosis": item["DIAGNOSIS"],
            "unchecked": len(cui),
            "cuis": cui
        }
        res.append(temp)
    return res


def getProgress(user, uid, progressConfig, dataConfig):
    f = open("index_id", "r")
    indexID = f.read()
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
    response = getResponse(progressConfig, url, query, header, "post")
    res = response.json()
    source = res["hits"]["hits"][0]["_source"]
    progress = json.loads(source["progress"])
    dataurl = dataConfig["URL"] + dataConfig["INDEX"] + "_doc/" + indexID
    dataRes = getResponse(dataConfig, dataurl, method="get")
    data = dataRes.json()
    dataContent = json.loads(data["_source"]["content"])
    allProgressDiagnosis = []
    for each in progress:
        allProgressDiagnosis.append(each["diagnosis"])
    for item in dataContent:
        if item["diagnosis"] not in allProgressDiagnosis:
            progress.append(item)
        else:
            for k in progress:
                if k["diagnosis"] == item["diagnosis"]:
                    for i in k["cuis"]:
                        for j in item["cuis"]:
                            if i["cui"] == j["cui"]:
                                j["rel"] = i["rel"]
                    k["cuis"] = item["cuis"]
    for p in progress:
        count = 0
        for cui in p["cuis"]:
            if cui["rel"] is None:
                count += 1
        p["unchecked"] = count
    progress.sort(key=lambda x: x["id"])
    res = {
        "user": user,
        "progress": json.dumps(progress, separators=(',', ':')),
        "finished": False
    }
    print(str(res))
    return res


def createProgress(data, progressConfig):
    header = {
        "Content-Type": "application/json"
    }
    url = progressConfig["URL"] + progressConfig["INDEX"] + "_doc/?refresh=true"
    response = getResponse(progressConfig, url, data, header, "post")
    res = response.json()
    return res


def updateProgress(uid, data, progressConfig):
    header = {
        "Content-Type": "application/json"
    }
    url = progressConfig["URL"] + progressConfig["INDEX"] + "_doc/" + uid + "?refresh=true"
    response = getResponse(progressConfig, url, data, header, "post")
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
    response = getResponse(progressConfig, url, query, header, "post")
    content = response.json()
    hit = content["hits"]["total"]["value"]
    if hit > 0:
        userId = content["hits"]["hits"][0]["_id"]
    else:
        userId = None
    return userId


def checkContentExistence(dataConfig):
    try:
        f = open("index_id", "r")
        indexID = f.read()
    except FileNotFoundError:
        indexID = None
    if indexID is not None and indexID != "":
        url = dataConfig["URL"] + dataConfig["INDEX"] + "_doc/" + indexID
        response = getResponse(dataConfig, url, method="get")
        if response is not None:
            content = response.json()
            if content["found"] is True:
                return content["_source"]["content"]
            else:
                return None
        else:
            return None
    else:
        return None


def updateContentInES(dataConfig, newContent, oriContent):
    f = open("index_id", "r")
    indexId = f.read()
    f.close()
    count = len(oriContent)
    allOldDiagnosis = []
    for item in oriContent:
        allOldDiagnosis.append(item["diagnosis"])
    for each in newContent:
        if each["diagnosis"] in allOldDiagnosis:
            for k in oriContent:
                if k["diagnosis"] == each["diagnosis"]:
                    k["cuis"] = each["cuis"]
        else:
            each["id"] = count + 1
            oriContent.append(each)
            count += 1
    data = {
        "doc": {
            "content": json.dumps(oriContent, separators=(',', ':'))
        },
        "detect_noop": False
    }
    header = {
        "Content-Type": "application/json"
    }
    url = dataConfig["URL"] + dataConfig["INDEX"] + "_update/" + indexId
    response = getResponse(dataConfig, url, data, header, "post")
    res = response.json()
    if res["result"] == "updated":
        print(str(datetime.datetime.now()) + "  Updated Successfully")
        f = open("update_log", "a+")
        f.write(str(datetime.datetime.now()) + "  Updated Successfully\n")
        f.close()
    else:
        print(str(datetime.datetime.now()) + "  Update Failed")
        f = open("update_log", "a+")
        f.write(str(datetime.datetime.now()) + "  Update Failed\n")
        f.close()


def addContent(dataConfig, content):
    uid = 1
    for each in content:
        each["id"] = uid
        uid += 1
    data = {
        "content": json.dumps(content, separators=(',', ':'))
    }
    header = {
        "Content-Type": "application/json"
    }
    url = dataConfig["URL"] + dataConfig["INDEX"] + "_doc"
    response = getResponse(dataConfig, url, data, header, "post")
    res = response.json()
    if res["result"] == "created":
        indexID = res["_id"]
        with open("index_id", "w+") as f:
            f.write(indexID)
            f.close()
    else:
        addContent(dataConfig, content)


def getFileContent(dataConfig):
    f = open("index_id", "r")
    indexID = f.read()
    url = dataConfig["URL"] + dataConfig["INDEX"] + "_doc/" + indexID
    response = getResponse(dataConfig, url, method="get")
    res = response.json()
    content = json.loads(res["_source"]["content"])
    content.sort(key=lambda x: x["id"])
    return content
