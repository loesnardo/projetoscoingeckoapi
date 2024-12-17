import requests
import time
import pandas as pd
import os

def get_valid_cryptos():
    """
    Obtém uma lista de criptomoedas válidas da API CoinGecko.
    
    Returns:
        list: Lista de criptomoedas válidas.
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 250,
            "page": 1
        }
        
        response = requests.get(url, params=params)
        
        # Verifica se o código de resposta foi 429 (muitas requisições)
        if response.status_code == 429:
            print("Limite de requisições excedido. Aguardando 30 segundos...")
            time.sleep(30)  # Espera 30 segundos antes de tentar novamente
            return get_valid_cryptos()  # Chama a função novamente após a espera
        
        response.raise_for_status()
        data = response.json()
        
        valid_cryptos = [crypto['id'] for crypto in data]
        
        return valid_cryptos
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar as criptomoedas válidas: {e}")
        return []

def get_valid_currencies():
    """
    Obtém uma lista de moedas-fiat válidas da API CoinGecko.
    
    Returns:
        list: Lista de moedas-fiat válidas.
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/supported_vs_currencies"
        
        response = requests.get(url)
        
        # Verifica se o código de resposta foi 429 (muitas requisições)
        if response.status_code == 429:
            print("Limite de requisições excedido. Aguardando 30 segundos...")
            time.sleep(30)  # Espera 30 segundos antes de tentar novamente
            return get_valid_currencies()  # Chama a função novamente após a espera
        
        response.raise_for_status()
        data = response.json()
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar as moedas-fiat válidas: {e}")
        return []

def get_crypto_prices(crypto_list, currency):
    """
    Busca os preços atuais das criptomoedas desejadas em uma moeda específica usando a API CoinGecko.
    
    Args:
        crypto_list (list): Lista das criptomoedas (ex.: ['bitcoin', 'ethereum']).
        currency (str): Moeda-fiat desejada (ex.: 'usd', 'brl').
    
    Returns:
        pd.DataFrame: DataFrame com os preços das criptomoedas.
    """
    try:
        # URL da API CoinGecko
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Parâmetros da requisição
        params = {
            "ids": ",".join(crypto_list),  # Junta as criptomoedas em uma string separada por vírgulas
            "vs_currencies": currency  # Moeda desejada
        }
        
        # Faz a requisição para a API
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lança um erro se a resposta tiver status diferente de 200
        
        # Converte os dados para JSON
        data = response.json()
        
        # Converte os dados em DataFrame para melhor visualização
        price_data = pd.DataFrame(data).T  # Transpõe para uma visualização adequada
        price_data = price_data.rename(columns={currency: f"Price ({currency.upper()})"})
        
        return price_data
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar os dados: {e}")
        return None

def fetch_and_display_prices(crypto_list, currency):
    """
    Função que busca e exibe os preços das criptomoedas escolhidas.
    
    Args:
        crypto_list (list): Lista das criptomoedas.
        currency (str): Moeda-fiat desejada.
    """
    print(f"\nBuscando os preços de {', '.join(crypto_list)} em {currency.upper()}...\n")
    price_data = get_crypto_prices(crypto_list, currency)
    
    if price_data is not None:
        print(price_data)
    else:
        print("Não foi possível buscar os preços.")

def validate_crypto_input(cryptos, valid_cryptos):
    """
    Valida se as criptomoedas inseridas são válidas.
    
    Args:
        cryptos (str): String com os nomes das criptomoedas inseridas pelo usuário.
        valid_cryptos (list): Lista de criptomoedas válidas obtidas da API.
    
    Returns:
        list: Lista de criptomoedas válidas ou None se inválido.
    """
    crypto_list = [crypto.strip().lower() for crypto in cryptos.split(",")]
    
    # Verifica se todas as criptomoedas são válidas
    if all(crypto in valid_cryptos for crypto in crypto_list):
        return crypto_list
    else:
        print("Uma ou mais criptomoedas inseridas não são válidas.")
        return None

def validate_currency_input(currency, valid_currencies):
    """
    Valida se a moeda-fiat inserida é válida.
    
    Args:
        currency (str): Moeda-fiat inserida pelo usuário.
        valid_currencies (list): Lista de moedas-fiat válidas.
    
    Returns:
        bool: True se a moeda for válida, caso contrário False.
    """
    return currency.lower() in valid_currencies

def reiniciar_programa():
    """Limpa o terminal."""
    # Limpa o terminal dependendo do sistema operacional
    if os.name == 'nt':  # Se for Windows
        os.system('cls')
    else:  # Se for Linux ou macOS
        os.system('clear')

def main():
    print("### Visualizador de Preço de Criptomoedas ###\n")
    
    # Obtenha as criptomoedas e moedas-fiat válidas da API
    valid_cryptos = get_valid_cryptos()
    valid_currencies = get_valid_currencies()
    
    if not valid_cryptos or not valid_currencies:
        print("Não foi possível obter as criptomoedas ou moedas-fiat válidas.")
        return
    
    # Inicializa as variáveis para as criptomoedas e a moeda
    crypto_list = []
    currency = ""
    
    # Entrada do usuário para criptomoedas e moeda
    cryptos = input("Digite as criptomoedas desejadas (separadas por vírgula, ex: bitcoin, ethereum): ").strip().lower()
    while not (crypto_list := validate_crypto_input(cryptos, valid_cryptos)):
        cryptos = input("Digite criptomoedas válidas (separadas por vírgula, ex: bitcoin, ethereum): ").strip().lower()
    
    currency = input("Digite a moeda-fiat desejada (ex: usd, brl): ").strip().lower()
    while not validate_currency_input(currency, valid_currencies):
        currency = input("Digite uma moeda válida (ex: usd, brl): ").strip().lower()

    # Exibe os preços pela primeira vez
    fetch_and_display_prices(crypto_list, currency)
    
    # Menu de opções
    while True:
        print("\nEscolha uma opção:")
        print("1. Repetir (buscar os mesmos preços)")
        print("2. Buscar novas (escolher novas criptomoedas e moeda)")
        print("3. Voltar (reiniciar o programa)")
        print("4. Sair")
        
        option = input("\nDigite o número da opção desejada: ").strip()
        
        if option == "1":
            fetch_and_display_prices(crypto_list, currency)
        
        elif option == "2":
            cryptos = input("\nDigite as criptomoedas desejadas (separadas por vírgula, ex: bitcoin, ethereum): ").strip().lower()
            while not (crypto_list := validate_crypto_input(cryptos, valid_cryptos)):
                cryptos = input("Digite criptomoedas válidas (separadas por vírgula, ex: bitcoin, ethereum): ").strip().lower()
            
            currency = input("Digite a moeda-fiat desejada (ex: usd, brl): ").strip().lower()
            while not validate_currency_input(currency, valid_currencies):
                currency = input("Digite uma moeda válida (ex: usd, brl): ").strip().lower()
            
            fetch_and_display_prices(crypto_list, currency)
        
        elif option == "3":
            print("Reiniciando o programa...\n")
            reiniciar_programa()
            main()  
            break
        
        elif option == "4":
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
