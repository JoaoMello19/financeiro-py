import pandas as pd
import plots
import tickers


TICKERS = ["AAPL", "PETR4.SA", "IVVB11.SA", "VALE3.SA", "BTC-USD"]
PERIOD = "1y"

for ticker in TICKERS:
    data = tickers.get_ticker_info(ticker, PERIOD)

    # Gerar gráficos
    if data is not None:
        plots.plot_last_closings(data, ticker, PERIOD)
        print(f"Gráficos gerados para {ticker}")

    # Salvar dados CSV
    df = pd.DataFrame(data)
    df.to_csv(f'./csv/{ticker}.csv')


print("Fim da execução")
