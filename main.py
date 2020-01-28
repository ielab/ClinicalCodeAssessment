from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonpify
from middleware import *
from waitress import serve
from werkzeug.utils import secure_filename
from methods import WaitressConfig, globalConfig, fileFormat
import sys, os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = globalConfig["UPLOADFOLDER"]
api = Api(app)


class uploadCSVFile(Resource):
    @staticmethod
    def post():
        if "file" not in request.files:
            res = jsonpify({"message": "No File Found In Request Body."})
            res.status_code = 400
            return res
        file = request.files["file"]
        if file.filename == '':
            res = jsonpify({"message": "No File Uploaded."})
            res.status_code = 400
            return res
        if file and fileFormat(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            res = jsonpify({"message": "File Upload Successfully."})
            res.status_code = 201
            return res
        else:
            res = jsonpify({"message": "File Type Is Not CSV."})
            res.status_code = 400
            return res


class getCUIInfos(Resource):
    @staticmethod
    def get():
        res = getCUIInfos()
        return jsonpify(res)


api.add_resource(uploadCSVFile, "/assess/upload")
api.add_resource(getCUIInfos, "/assess/info")

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
