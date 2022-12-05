from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

metrics_get_args = reqparse.RequestParser()
# metrics_get_args.add

class Metrics(Resource):
    def get(self, metrics_name):
        metrics = {}
        with open("db/cpu.json", "r") as f:
            data = json.load(f)
            # print(data["cpu"])
            metrics = data[metrics_name]
        # print(metrics)
        return metrics


api.add_resource(Metrics, '/<string:metrics_name>')

if __name__ == '__main__':
    app.run(debug=True)