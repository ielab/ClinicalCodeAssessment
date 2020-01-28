import os


def removeUploadedFile():
    directory = "data"
    for path in os.listdir(directory):
        p = os.path.join(directory, path)
        if os.path.isfile(p):
            os.remove(p)


def getCUIConcepts(content):
    return
