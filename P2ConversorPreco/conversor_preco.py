import requests
import time # Importar o módulo time para adicionar o sleep
import os  

def get_valid_cryptos():
    """
    Obtém uma lista de moedas válidas (criptomoedas e fiduciárias) da API CoinGecko.
    """
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        dados = resposta.json()
        # Retorna os IDs das moedas válidas
        return [moeda['id'] for moeda in dados]
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar moedas válidas: {e}")
        return []

def moeda_valida(moeda, lista_validas):
    """
    Verifica se a moeda está na lista de moedas válidas.
    """
    return moeda in lista_validas

def obter_preco_moeda(moeda, referencia="usd"):
    """
    Obtém o preço atual da moeda (criptomoeda ou fiduciária) em relação à moeda de referência.
    Se o limite de requisições for excedido (429), aguarda 30 segundos e tenta novamente.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={moeda}&vs_currencies={referencia}"
    
    try:
        resposta = requests.get(url)
        
        # Verifica se o limite de requisições foi excedido
        if resposta.status_code == 429:
            print("Limite de requisições excedido. Aguardando 30 segundos...")
            time.sleep(30)  # Aguarda 30 segundos antes de tentar novamente
            return obter_preco_moeda(moeda, referencia)  # Tenta novamente
        
        resposta.raise_for_status()  # Lança um erro se o status não for 200
        dados = resposta.json()
        
        return dados.get(moeda, {}).get(referencia)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

def conversao_indireta(moeda_origem, moeda_destino, valor_origem):
    """
    Realiza a conversão de uma moeda de origem para uma moeda de destino.
    """
    preco_origem = obter_preco_moeda(moeda_origem)
    preco_destino = obter_preco_moeda(moeda_destino)

    if preco_origem is None or preco_destino is None:
        print(f"Erro: Não foi possível encontrar os preços para {moeda_origem} ou {moeda_destino}.")
        return None

    # Calcular a taxa de conversão entre as moedas
    taxa_conversao = preco_origem / preco_destino
    return valor_origem * taxa_conversao

def reiniciar_programa():
    """Limpa o terminal."""
    # Limpa o terminal dependendo do sistema operacional
    if os.name == 'nt':  # Se for Windows
        os.system('cls')
    else:  # Se for Linux ou macOS
        os.system('clear')

def main():
    print("Conversor de Criptomoedas e Moedas Fiat (Não é possivel converter fiat para fiat)")
    
    lista_validas = get_valid_cryptos()
    if not lista_validas:
        print("Erro ao carregar as moedas válidas. Encerrando o programa.")
        return
    
    while True:  # Loop principal
        # Entrada da moeda de origem
        moeda_origem = ""
        while not moeda_valida(moeda_origem, lista_validas):
            moeda_origem = input("\nDigite a moeda de origem (ex: bitcoin, ethereum, usd, brl): ").lower()
            if not moeda_valida(moeda_origem, lista_validas):
                print("Erro: Moeda de origem inválida. Tente novamente.")

        # Entrada da moeda de destino
        moeda_destino = ""
        while not moeda_valida(moeda_destino, lista_validas):
            moeda_destino = input("Digite a moeda de destino (ex: bitcoin, ethereum, usd, brl): ").lower()
            if not moeda_valida(moeda_destino, lista_validas):
                print("Erro: Moeda de destino inválida. Tente novamente.")

        # Entrada do valor da moeda de origem
        valor_origem = -1
        while valor_origem <= 0:
            try:
                valor_origem = float(input("Digite o valor da moeda de origem: "))
                if valor_origem <= 0:
                    print("Erro: O valor deve ser maior que zero. Tente novamente.")
            except ValueError:
                print("Erro: Valor inválido. Digite um número válido.")

        # Realiza a conversão
        valor_convertido = conversao_indireta(moeda_origem, moeda_destino, valor_origem)
        
        if valor_convertido is not None:
            print(f"\n{valor_origem} {moeda_origem.upper()} equivale a {valor_convertido:.6f} {moeda_destino.upper()}.")

        # Opções do usuário
        while True:
            print("\nO que você deseja fazer?")
            print("1 - Fazer outra conversão")
            print("2 - Reiniciar")
            print("3 - Sair")
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "3":
                print("Saindo...")
                exit()  # Sai imediatamente do programa
            elif opcao == "2":
                 print("Reiniciando o programa...\n")
                 reiniciar_programa()
                 main()  
                 break
            elif opcao == "1":
                break  # Retorna ao loop principal
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

