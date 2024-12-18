import requests
import pandas as pd


def get_top_10_cryptos(currency):
    """
    Busca as top 10 criptomoedas por capitalização de mercado.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': currency,
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return []


def format_data(cryptos, currency):
    """
    Formata os dados retornados pela API em um DataFrame.
    """
    df = pd.DataFrame(cryptos, columns=['name', 'current_price', 'total_volume', 'price_change_percentage_24h'])
    df.columns = ['Nome', f'Preço ({currency.upper()})', f'Volume 24h ({currency.upper()})', 'Variação 24h (%)']

    # Formatar dados com valores válidos
    df['Variação 24h (%)'] = df['Variação 24h (%)'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "N/A")
    df[f'Preço ({currency.upper()})'] = df[f'Preço ({currency.upper()})'].apply(
        lambda x: f"{x:,.8f} {currency.upper()}" if x < 1 else f"{x:,.2f} {currency.upper()}"
    )
    df[f'Volume 24h ({currency.upper()})'] = df[f'Volume 24h ({currency.upper()})'].apply(
        lambda x: f"{x:,.2f} {currency.upper()}" if pd.notnull(x) else "N/A"
    )

    return df


def display_table(df):
    """
    Exibe os dados formatados no terminal.
    """
    print(f"{'Posição':<10} {'Nome':<20} {df.columns[1]:>15} {df.columns[2]:>20} {df.columns[3]:>20}")
    print("-" * 100)

    for index, row in df.iterrows():
        print("")  # Linha em branco para espaçamento
        print(f"{index + 1:<10} {row['Nome']:<20} {row[df.columns[1]]:>15} {row[df.columns[2]]:>20} {row[df.columns[3]]:>20}")
        print("-" * 100)  # Linha separadora
   


def main():
    print("Digite a moeda base para exibir os preços (ex.: brl, usd):")
    user_currency = input().strip().lower()

    cryptos = get_top_10_cryptos(user_currency)
    if cryptos:
        df = format_data(cryptos, user_currency)
        display_table(df)
    else:
        print("Não foi possível obter os dados. Verifique sua conexão ou tente novamente mais tarde.")


if __name__ == "__main__":
    main()
