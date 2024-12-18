from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Função para obter as 10 principais criptomoedas
# Função para obter as 10 principais criptomoedas
def get_top_10_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        cryptos = response.json()
        
        # Adicionar o volume de 24 horas em cada criptomoeda
        for crypto in cryptos:
            coin_id = crypto['id']
            # Obter o volume de 24 horas
            coin_data = get_coin_market_chart(coin_id, days=1)  # Passando 1 dia para pegar dados do último dia
            if coin_data and "total_volumes" in coin_data:
                # Pega o volume mais recente
                latest_volume = coin_data["total_volumes"][-1][1] if coin_data["total_volumes"] else 0
                crypto['volume_24h'] = latest_volume
            else:
                crypto['volume_24h'] = 0
        
        return cryptos
    return []


# Função para obter os preços históricos de uma moeda
def get_coin_market_chart(coin_id, days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {}

@app.route("/")
def index():
    top_cryptos = get_top_10_cryptos()
    return render_template("index.html", cryptos=top_cryptos)

@app.route("/coin/<coin_id>")
def coin_details(coin_id):
    data = get_coin_market_chart(coin_id)
    
    if not data or "prices" not in data:
        return render_template("coin_details.html", coin_id=coin_id, error="No data available", dates=[], values=[])
    
    # Extrair datas e valores
    prices = data["prices"]
    dates = [entry[0] for entry in prices]  # Timestamps
    values = [entry[1] for entry in prices]  # Valores de preço
    
    return render_template("coin_details.html", coin_id=coin_id, dates=json.dumps(dates), values=json.dumps(values), error=None)

if __name__ == "__main__":
    app.run(debug=True)
