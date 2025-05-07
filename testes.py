import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tickers
import os

# --- Constantes ---
TICKERS = ["AAPL", "PETR4.SA", "IVVB11.SA", "VALE3.SA", "BTC-USD"]
PERIOD = '6mo'
INVEST = 1_000_000
CSV_OUTPUT = './csv/results.csv'
GRAPH_DIR = './graficos'

CONDITIONS = [
    ("raised[i]", lambda r, n, i: r[i]),
    ("not raised[i]", lambda r, n, i: not r[i]),
    ("raised[i] or raised[i-1]", lambda r, n, i: r[i] or r[i-1]),
    ("not (raised[i] or raised[i-1])", lambda r, n, i: not (r[i] or r[i-1])),
    ("raised[i] and raised[i-1]", lambda r, n, i: r[i] and r[i-1]),
    ("not (raised[i] and raised[i-1])", lambda r, n, i: not (r[i] and r[i-1])),
    ("next[i]", lambda r, n, i: n[i]),
]

# --- Funções ---

def load_data(ticker, period):
    """Carrega e prepara os dados de um ticker."""
    data = tickers.get_ticker_info(ticker, period)
    data = data[['Close', '% Change', 'Delta_MM', 'Raised', 'Next Raised']]
    return data.dropna()


def simular_estrategia(data, condition_func):
    """Executa a simulação da estratégia com base na condição fornecida."""
    close = data['Close'].to_list()
    raised = data['Raised'].to_list()
    nexts = data['Next Raised'].to_list()

    montante = INVEST
    num_acoes = 0
    valores = []

    for i in range(1, len(close)):
        if condition_func(raised, nexts, i) and close[i] > 0:
            num_acoes += montante // close[i]
            montante %= close[i]
        else:
            montante += close[i] * num_acoes
            num_acoes = 0
        valores.append(montante + close[i] * num_acoes)

    return valores


def registrar_resultados(ticker, condition_string, valores, resultados):
    """Adiciona os resultados da simulação ao dicionário final."""
    if not valores:
        return

    resultados['ticker'].append(ticker)
    resultados['condition'].append(condition_string)
    resultados['inicio'].append(INVEST)
    resultados['minimo'].append(min(valores))
    resultados['maximo'].append(max(valores))
    resultados['final'].append(valores[-1])
    resultados['variacao'].append((valores[-1] / INVEST - 1) * 100)


def gerar_grafico(df, y_col, titulo, ylabel, filename, ylim=None):
    """Gera e salva um gráfico de barras agrupado."""
    plt.figure(figsize=(14, 7))
    sns.barplot(x='ticker', y=y_col, hue='condition', data=df)
    plt.title(titulo)
    plt.xlabel('Ticker')
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Condição')
    if y_col == 'variacao':
        plt.axhline(0, color='grey', linestyle='--', linewidth=0.8)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
    if ylim:
        plt.ylim(*ylim)
    plt.tight_layout()
    os.makedirs(GRAPH_DIR, exist_ok=True)
    plt.savefig(os.path.join(GRAPH_DIR, filename))


# --- Execução Principal ---

def main():
    resultados = {
        'ticker': [],
        'condition': [],
        'inicio': [],
        'maximo': [],
        'minimo': [],
        'final': [],
        'variacao': [],
    }

    for ticker in TICKERS:
        for condition_string, condition_func in CONDITIONS:
            data = load_data(ticker, PERIOD)
            if len(data) < 2:
                print(f"Dados insuficientes para {ticker} com a condição '{condition_string}'. Pulando.")
                continue

            valores = simular_estrategia(data, condition_func)
            registrar_resultados(ticker, condition_string, valores, resultados)

    df = pd.DataFrame(resultados)
    os.makedirs(os.path.dirname(CSV_OUTPUT), exist_ok=True)
    df.to_csv(CSV_OUTPUT, index=False)

    gerar_grafico(df, 'final', 'Valor Final do Portfólio por Ticker e Condição', 'Valor Final', 'grafico_final.png')
    gerar_grafico(df, 'variacao', 'Variação Percentual do Portfólio por Ticker e Condição', 'Variação (%)', 'grafico_variacao.png', ylim=(-50, 400))


if __name__ == "__main__":
    main()
