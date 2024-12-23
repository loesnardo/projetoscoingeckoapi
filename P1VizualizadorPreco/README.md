# Visualizador de Preço de Criptomoedas

Este é um **visualizador de preços de criptomoedas** em tempo real, utilizando a API gratuita da **CoinGecko** para consultar os preços de diversas criptomoedas em várias moedas-fiat (USD, BRL, etc.). O projeto foi desenvolvido com **Python**, utilizando as bibliotecas **requests** e **pandas**.

## Funcionalidades

- O usuário pode consultar os preços em tempo real de uma lista específica de criptomoedas.
- Os preços podem ser exibidos em várias moedas-fiat, como **USD**, **BRL**, entre outras.
- A visualização dos dados é feita através de uma tabela gerada pelo **pandas**.

## Tecnologias Utilizadas

- **Python 3**
- **requests** (para realizar requisições HTTP)
- **pandas** (para manipulação e visualização de dados)

## Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina. Para instalar as dependências necessárias, execute:

```bash
pip install requests pandas
```

## Como Executar o Projeto

1. Clone este repositório para o seu ambiente local:

```bash
git clone https://github.com/loesnardo/projetoscoingeckoapi.git
```

2. Navegue até o diretório do projeto:

```bash
cd projetoscoingeckoapi/P1VizualizadorPreco
```

3. Execute o script:

```bash
python visualizador_preco.py
```

4. Insira a lista de criptomoedas e a moeda-fiat desejada. Exemplo de entrada:

```
Digite as criptomoedas desejadas (separadas por vírgula, ex: bitcoin,ethereum): bitcoin,ethereum
Digite a moeda-fiat desejada (ex: usd, brl): usd
```

5. O script retornará uma tabela com os preços das criptomoedas inseridas.

## Exemplo de Saída

Após a execução, você verá algo assim:

```
            Price (USD)
bitcoin       107345.21
ethereum       4000.32
solana          200.44
```


