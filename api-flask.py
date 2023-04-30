from flask import Flask
import requests as req
import json
from datetime import datetime

# Larissa Ionafa RA: 1903166

app = Flask(__name__)

# VIA CEP
@app.route('/cep/<cep>', methods=['GET'])
def search_cep(cep):
    response = req.get(f'https://viacep.com.br/ws/{cep}/json/')
    return response.text

# COTAÇÃO DE MOEDAS
@app.route('/cotacao/<moeda>', methods=['GET'])
def search_moeda(moeda):
    resp = req.get(f'https://economia.awesomeapi.com.br/last/{moeda}').text
    resp = json.loads(resp)
    moeda_pair = moeda.replace("-", "")
    response = {
        "source_moeda": resp[moeda_pair]["code"],
        "destination_moeda": resp[moeda_pair]["codein"],
        "moeda_name": resp[moeda_pair]["name"],
        "max_value": resp[moeda_pair]["high"],
        "min_value": resp[moeda_pair]["low"],
        "moeda_date": resp[moeda_pair]["create_date"],
    }
    return response

@app.route('/cotacao/<moeda>/<days>', methods=['GET'])
def search_moeda_days(moeda, days=1):
    resp = req.get(f"https://economia.awesomeapi.com.br/json/daily/{moeda}/{days}").text
    resp = json.loads(resp)
    response = []
    for data in resp:
        date_obj = datetime.fromtimestamp(int(data.get('timestamp', 0)))
        formatted_date = date_obj.strftime('%Y-%m-%d')
        response.append(
    {
        "value": data.get('high', 0),
        "date": formatted_date
    }
)

    return response


@app.route('/convert/<moeda>/<value>', methods=['GET'])
def convert(moeda, value):
    url = f'https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,BTC-BRL,ARS-BRL'
    response = requests.get(url)
    data = response.json()

    if moeda == 'USD':
        converted_value = float(value) * float(data['USDBRL']['bid'])
        result = f'{value} USD = {converted_value:.2f} BRL'
    elif moeda == 'EUR':
        converted_value = float(value) * float(data['EURBRL']['bid'])
        result = f'{value} EUR = {converted_value:.2f} BRL'
    elif moeda == 'BTC':
        converted_value = float(value) * float(data['BTCBRL']['bid'])
        result = f'{value} BTC = {converted_value:.2f} BRL'
    elif moeda == 'ARS':
        converted_value = float(value) * float(data['ARSBRL']['bid'])
        result = f'{value} ARS = {converted_value:.2f} BRL'
    else:
        result = f'Invalid moeda: {moeda}'

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
