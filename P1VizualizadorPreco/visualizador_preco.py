import requests
import pandas as pd

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

def main():
    print("### Visualizador de Preço de Criptomoedas ###\n")
    
    # Variáveis para armazenar as criptomoedas e moeda escolhidas
    crypto_list = []
    currency = ""
    
    # Entrada do usuário para as criptomoedas e moeda
    cryptos = input("Digite as criptomoedas desejadas (separadas por vírgula, ex: bitcoin,ethereum): ").strip().lower()
    currency = input("Digite a moeda-fiat desejada (ex: usd, brl): ").strip().lower()
    
    # Processa a lista de criptomoedas
    crypto_list = [crypto.strip() for crypto in cryptos.split(",")]
    
    print(f"\nBuscando os preços de {', '.join(crypto_list)} em {currency.upper()}...\n")
    
    # Busca os preços
    price_data = get_crypto_prices(crypto_list, currency)
    
    if price_data is not None:
        print(price_data)
    else:
        print("Não foi possível buscar os preços.")
    
    # Menu de opções após a primeira execução
    while True:
        print("\nEscolha uma opção:")
        print("1. Repetir (buscar os mesmos preços)")
        print("2. Buscar novas (escolher novas criptomoedas e moeda)")
        print("3. Sair")
        
        option = input("\nDigite o número da opção desejada: ").strip()
        
        if option == "1":
            if not crypto_list or not currency:
                print("Nenhuma criptomoeda ou moeda foi escolhida ainda. Escolha novas opções.")
                continue
            
            print(f"\nBuscando os preços de {', '.join(crypto_list)} em {currency.upper()}...\n")
            price_data = get_crypto_prices(crypto_list, currency)
            
            if price_data is not None:
                print(price_data)
            else:
                print("Não foi possível buscar os preços.")
        
        elif option == "2":
            # Entrada do usuário para novas criptomoedas e moeda
            cryptos = input("\nDigite as criptomoedas desejadas (separadas por vírgula, ex: bitcoin,ethereum): ").strip().lower()
            currency = input("Digite a moeda-fiat desejada (ex: usd, brl): ").strip().lower()
            
            # Processa a lista de criptomoedas
            crypto_list = [crypto.strip() for crypto in cryptos.split(",")]
            
            print(f"\nBuscando os preços de {', '.join(crypto_list)} em {currency.upper()}...\n")
            price_data = get_crypto_prices(crypto_list, currency)
            
            if price_data is not None:
                print(price_data)
            else:
                print("Não foi possível buscar os preços.")
        
        elif option == "3":
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()