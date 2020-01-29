import os
import requests
import json


def removeUploadedFile():
    directory = "data"
    for path in os.listdir(directory):
        p = os.path.join(directory, path)
        if os.path.isfile(p):
            os.remove(p)


def getCUIPreferredTerm(cui):
    return cui


def getCUIPreferredTerms(content, globalConfig):
    # res = []
    # for item in content:
    #     cuiSet = item["CUI_SET"]
    #     for cui in cuiSet:
            # response = requests.get(globalConfig["ES"]["URL"] + '?pretty&q=_id=' + cui, )
            # print(response.content)
            # content = json.loads(response.content)
            # prefTerm = content["hits"]["hits"]["_source"]["thesaurus"][0]["MRCONSO_STR"]
            # print(prefTerm)
    return content

# https://ielab:gUCt8MbTKJasmMqpKNBQ@ielab-sysrev1.uqcloud.net/_search?pretty&q=_id=C0000139