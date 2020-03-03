import sys
from flask import Flask, request
from flask_cors import CORS
from flask_jsonpify import jsonpify
from flask_restful import Resource, Api
from waitress import serve
from apscheduler.schedulers.background import BackgroundScheduler
from middleware import *

# Two empty ES Index should be created beforehand, progress index and data index

with open('Config.json') as configFile:
    config = json.load(configFile)
scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=updateContent, trigger="interval", seconds=config["UPDATE_INTERVAL"])
scheduler.start()


app = Flask(__name__)
CORS(app)
api = Api(app)


class getFileContent(Resource):
    @staticmethod
    def get():
        res = jsonpify(getContent())
        res.status_code = 200
        return res


class getProgress(Resource):
    @staticmethod
    def get():
        user = request.args["u"]
        uid = request.args["uid"]
        res = jsonpify(getUserProgress(user, uid))
        res.status_code = 200
        return res


class createProgress(Resource):
    @staticmethod
    def post():
        data = request.json
        res = jsonpify(createUserProgress(data))
        res.status_code = 201
        return res


class updateProgress(Resource):
    @staticmethod
    def post():
        uid = request.args["uid"]
        data = request.json
        res = jsonpify(updateUserProgress(uid, data))
        res.status_code = 200
        return res


class getUserID(Resource):
    @staticmethod
    def get():
        user = request.args["u"]
        res = jsonpify(getUserId(user))
        res.status_code = 200
        return res


api.add_resource(getFileContent, "/assess/content")
api.add_resource(getProgress, "/assess/progress/get")
api.add_resource(updateProgress, "/assess/progress/update")
api.add_resource(createProgress, "/assess/progress/create")
api.add_resource(getUserID, "/assess/userid")

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) == 1:
        # Development server debug mode
        app.config["DEBUG"] = True
        print("App run in dev mode on port: ", WaitressConfig["PORT"])
        app.run(port=WaitressConfig["PORT"])
    elif len(arguments) == 2 and (arguments[1] == "--dev" or arguments[1] == "-d"):
        # Development server debug mode
        app.config["DEBUG"] = True
        print("App run in dev mode on port: ", WaitressConfig["PORT"])
        app.run(port=WaitressConfig["PORT"])
    elif len(arguments) == 2 and (arguments[1] == "--prod" or arguments[1] == "-p"):
        # Construct the production server using waitress
        # can be configured through changing in Config.json
        serve(
            app,
            host=WaitressConfig["HOST"],
            port=WaitressConfig["PORT"],
            ipv4=WaitressConfig["IPV4"],
            ipv6=WaitressConfig["IPV6"],
            threads=WaitressConfig["THREADS"],
            url_scheme=WaitressConfig["URLSCHEME"]
        )
    else:
        print("Wrong arguments, please check your input.")
