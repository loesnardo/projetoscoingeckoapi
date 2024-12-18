import requests
import plotly.graph_objects as go
from datetime import datetime, timezone

# Função para buscar dados históricos do CoinGecko
def fetch_crypto_prices(crypto_id, vs_currency, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados: {e}")
        return None

# Função para processar os dados
def process_data(data):
    daily_prices = {}
    for price in data["prices"]:
        timestamp = price[0] // 1000
        date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime('%Y-%m-%d')
        price_value = price[1]
        daily_prices.setdefault(date, []).append(price_value)
    dates, avg_prices = zip(*[(date, sum(prices) / len(prices)) for date, prices in daily_prices.items()])
    return dates, avg_prices

# Função para plotar o gráfico interativo
def plot_crypto_prices_plotly(dates, prices, crypto_name, vs_currency):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=prices, 
        mode='lines+markers',
        name=crypto_name,
        line=dict(color='royalblue', width=2),
        marker=dict(size=8, color='blue'),
        hovertemplate='Data: %{x}<br>Preço: %{y:.2f} ' + vs_currency.upper() + '<extra></extra>'
    ))
    fig.update_layout(
        title=f'Histórico de Preço - {crypto_name}',
        xaxis_title='Data',
        yaxis_title=f'Preço ({vs_currency.upper()})',
        xaxis=dict(tickangle=45),
        template='plotly_white',
        hovermode="x unified"
    )
    fig.show()

# Função para validar criptomoeda
def validate_crypto_id(crypto_id):
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        coins = response.json()
        return any(coin["id"] == crypto_id for coin in coins)
    except requests.RequestException as e:
        print(f"Erro ao validar criptomoeda: {e}")
        return False

# Função para validar moeda fiduciária
def validate_vs_currency(vs_currency):
    url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
    try:
        response = requests.get(url)
        response.raise_for_status()
        currencies = response.json()
        return vs_currency in currencies
    except requests.RequestException as e:
        print(f"Erro ao validar moeda fiduciária: {e}")
        return False

# Função para obter entradas válidas do usuário
def get_valid_user_input():
    while True:
        crypto_id = input("Digite o ID da criptomoeda (ex: bitcoin, ethereum): ").strip().lower()
        if not validate_crypto_id(crypto_id):
            print("Criptomoeda inválida. Tente novamente.")
            continue

        vs_currency = input("Digite a moeda fiduciária (ex: usd, brl, eur): ").strip().lower()
        if not validate_vs_currency(vs_currency):
            print("Moeda fiduciária inválida. Tente novamente.")
            continue

        days = input("Digite o intervalo de tempo em dias (ex: 7, 30, 90): ").strip()
        try:
            days = int(days)
            if days <= 0:
                raise ValueError
        except ValueError:
            print("Intervalo inválido. Digite um número inteiro positivo.")
            continue

        return crypto_id, vs_currency, days

# Main
if __name__ == "__main__":
    crypto_id, vs_currency, days = get_valid_user_input()
    data = fetch_crypto_prices(crypto_id, vs_currency, days)
    if data:
        dates, avg_prices = process_data(data)
        plot_crypto_prices_plotly(dates, avg_prices, crypto_id.capitalize(), vs_currency)
