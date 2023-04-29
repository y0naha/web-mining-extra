from flask import Flask, jsonify
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

# VIA CEP
class Cep(Resource):
    def get(self, cep):
        url = f"https://viacep.com.br/ws/{cep}/json/"
        response = requests.get(url)
        data = response.json()
        return jsonify(data)

api.add_resource(Cep, "/cep/<cep>")

# COTAÇÃO DE MOEDAS

@app.route('/convert/<currency>/<value>', methods=['GET'])
def convert(currency, value):
    url = f'https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL,ARS-BRL'
    response = requests.get(url)
    data = response.json()

    if currency == 'USD':
        converted_value = float(value) * float(data['USDBRL']['bid'])
        result = f'{value} USD = {converted_value:.2f} BRL'
    elif currency == 'EUR':
        converted_value = float(value) * float(data['EURBRL']['bid'])
        result = f'{value} EUR = {converted_value:.2f} BRL'
    elif currency == 'BTC':
        converted_value = float(value) * float(data['BTCBRL']['bid'])
        result = f'{value} BTC = {converted_value:.2f} BRL'
    elif currency == 'ARS':
        converted_value = float(value) * float(data['ARSBRL']['bid'])
        result = f'{value} ARS = {converted_value:.2f} BRL'
    else:
        result = f'Invalid currency: {currency}'

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
