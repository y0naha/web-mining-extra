from flask import Flask
import requests as req
import json
from datetime import datetime
import pytz

app = Flask(__name__)

# VIA CEP
@app.route('/cep/<cep>', methods=['GET'])
def search_cep(cep):
    response = req.get(f'https://viacep.com.br/ws/{cep}/json/')
    return response.text

# COTAÇÃO DE MOEDAS
@app.route('/cotacao/<currency>', methods=['GET'])
def search_currency(currency):
    resp = req.get(f'https://economia.awesomeapi.com.br/last/{currency}').text
    resp = json.loads(resp)
    currency_pair = currency.replace("-", "")
    response = {
        "source_currency": resp[currency_pair]["code"],
        "destination_currency": resp[currency_pair]["codein"],
        "currency_name": resp[currency_pair]["name"],
        "max_value": resp[currency_pair]["high"],
        "min_value": resp[currency_pair]["low"],
        "currency_date": resp[currency_pair]["create_date"],
    }
    return response

@app.route('/cotacao/<currency>/<days>', methods=['GET'])
def search_currency_days(currency, days=1):
    resp = req.get(f"https://economia.awesomeapi.com.br/json/daily/{currency}/{days}").text
    resp = json.loads(resp)
    response = []
    for data in resp:
        dt = datetime.fromtimestamp(int(data['timestamp']))
        br_tz = pytz.timezone('America/Sao_Paulo')
        dt_br = dt.astimezone(br_tz)
        formatted_date = dt_br.strftime('%Y-%m-%d %H:%M:%S %Z%z')
        response.append(
            {
                "value": data['high'],
                "date": formatted_date.split(" ")[0]
            }
        )
    return response

if __name__ == '__main__':
    app.run(debug=True)
