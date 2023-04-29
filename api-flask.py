from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

class Cep(Resource):
    def get(self, cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        data = response.json()
        return jsonify(data)

api.add_resource(Cep, "/cep/<cep>")

if __name__ == "__main__":
    app.run(debug=True)
