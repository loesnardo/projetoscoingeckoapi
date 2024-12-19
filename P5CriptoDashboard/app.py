from flask import Flask, render_template, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# Função de dados para rota principal
def get_top_10_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

@app.route('/')
def index():
    cryptos = get_top_10_cryptos()
    year = datetime.now().year
    return render_template('index.html', cryptos=cryptos, year=year)

@app.route('/coin/<coin_id>')
def coin_details(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": 30}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        dates = [price[0] for price in prices]
        values = [price[1] for price in prices]
        year = datetime.now().year
        return render_template('coin_details.html', coin_id=coin_id, dates=dates, values=values, year=year)
    else:
        return render_template('coin_details.html', coin_id=coin_id, error="Data not available", year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)
