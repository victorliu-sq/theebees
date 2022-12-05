from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

class Metrics(Resource):
    def get(self, req_metrics):
        results = {}
        with open("db/cpu.json", "r") as f:
            data = json.load(f)
            # print(data["cpu"])
            for m in req_metrics.split(","):
                results[m] = data[m]
        print(results)
        return results

api.add_resource(Metrics, '/<string:req_metrics>')

if __name__ == '__main__':
    app.run(debug=True)