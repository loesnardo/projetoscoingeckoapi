Aqui está o README seguindo o modelo solicitado para o seu projeto:

```markdown
# Conversor de Criptomoedas e Moedas Fiat

Este é um **conversor de criptomoedas e moedas fiduciárias** (como USD, BRL, etc.)(No Momento so não é possivel converter de fiat para fiat), utilizando a API gratuita da **CoinGecko** para consultar os preços e realizar conversões entre diferentes moedas. O projeto foi desenvolvido com **Python**, utilizando a biblioteca **requests**.

## Funcionalidades

- O usuário pode converter valores de uma moeda de origem para uma moeda de destino (ex: Bitcoin para USD, Ethereum para Bitcoin, BRL para Bitcoin).
- Suporta diversas criptomoedas e moedas fiduciárias (USD,  BRL, etc.).
- O programa realiza a verificação da validade das moedas antes de realizar a conversão.
- Caso o limite de requisições à API seja excedido, o programa aguarda 30 segundos e tenta novamente.

## Tecnologias Utilizadas

- **Python 3**
- **requests** (para realizar requisições HTTP)

## Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina. Para instalar as dependências necessárias, execute:

```bash
pip install requests
```

## Como Executar o Projeto

1. Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/loesnardo/projetoscoingeckoapi.git
```

2. Navegue até o diretório do projeto:

```bash
cd projetoscoingeckoapi/P2ConversorPreco
```

3. Execute o script:

```bash
python conversor_preco.py
```

4. O programa solicitará que você insira a moeda de origem, a moeda de destino e o valor da moeda de origem. Exemplo de entrada:

```
Digite a moeda de origem (ex: bitcoin, ethereum, usd, brl): bitcoin
Digite a moeda de destino (ex: bitcoin, ethereum, usd, brl): usd
Digite o valor da moeda de origem: 1
```

5. O script realizará a conversão e exibirá o valor convertido. Exemplo de saída:

```
1 BITCOIN equivale a 23450.123456 USD.
```

6. O programa oferecerá opções para:
   - Fazer outra conversão
   - Reiniciar o programa
   - Sair do programa

## Exemplo de Saída

Após a execução, você verá algo assim:

```
Conversor de Criptomoedas e Moedas Fiat (Não é possível converter fiat para fiat)

Digite a moeda de origem (ex: bitcoin, ethereum, usd, brl): bitcoin
Digite a moeda de destino (ex: bitcoin, ethereum, usd, brl): usd
Digite o valor da moeda de origem: 1

1 BITCOIN equivale a 23450.123456 USD.

O que você deseja fazer?
1 - Fazer outra conversão
2 - Reiniciar
3 - Sair
Escolha uma opção: 1
```

## Funções

### `get_valid_cryptos()`
Obtém a lista de moedas válidas da API do CoinGecko.

### `moeda_valida(moeda, lista_validas)`
Verifica se uma moeda fornecida está na lista de moedas válidas.

### `obter_preco_moeda(moeda, referencia="usd")`
Obtém o preço atual de uma moeda em relação a uma moeda de referência.

### `conversao_indireta(moeda_origem, moeda_destino, valor_origem)`
Realiza a conversão de uma moeda de origem para uma moeda de destino com base nos preços obtidos da API.

### `reiniciar_programa()`
Limpa o terminal dependendo do sistema operacional (Windows ou Linux/macOS).

### `main()`
Função principal que gerencia a interação com o usuário, realiza a conversão e oferece opções para continuar, reiniciar ou sair.
