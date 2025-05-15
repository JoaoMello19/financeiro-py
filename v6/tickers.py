import numpy as np
import yfinance as yf


def get_ticker_data(ticker_name: str, period: str = "1y"):
    """
    Retorna um DataFrame com os dados de um ticker.
    """
    ticker = yf.Ticker(ticker_name)
    data = ticker.history(period=period)[['Open', 'High', 'Low', 'Close', 'Volume']]

    if data.empty:
        return None

    # adiciona as colunas com dia, mês e ano
    data["Day"] = data.index.day
    data["Month"] = data.index.month
    data["Year"] = data.index.year

    # altera o tipo de índice apenas para data (yyyy-mm-dd)
    data.index = data.index.date
    data.index.name = "Date"

    # diferença percentual
    data["% Change"] = data["Close"].pct_change() * 100

    # médias móveis
    data['MM_7']  = data['Close'].rolling(window=7).mean()
    data['MM_15'] = data['Close'].rolling(window=15).mean()

    # diferença das médias móveis
    data["Delta_7"]  = data["Close"] - data['MM_7']
    data["Delta_15"] = data["Close"] - data['MM_15']
    data['Delta_MM'] = data['MM_7'] - data["MM_15"]

    # lags (dados de dias anteriores)
    data['Lag_1'] = data['Close'].shift(-1)
    data['Lag_2'] = data['Close'].shift(-2)
    data['Lag_3'] = data['Close'].shift(-3)
    data['Lag_4'] = data['Close'].shift(-4)
    data['Lag_5'] = data['Close'].shift(-5)

    # oscilação (subiu ou desceu)
    data['Raised'] = np.where(data["% Change"] > 0, 1, 0)
    data['Next Raised'] = np.where(data["% Change"].shift(-1) > 0, 1, 0)

    # retorna apenas os dados válidos
    return data.dropna()


# Cria os arquivos CSV dos tickers escolhidos
if __name__ == "__main__":
    TICKERS = ["AAPL", "PETR4.SA", "IVVB11.SA", "VALE3.SA", "BTC-USD"]
    PERIOD  = "1y"

    for ticker in TICKERS:
        data = get_ticker_data(ticker, PERIOD)

        # Salvar dados CSV
        if data is not None:
            data.to_csv(f'./csv/{ticker}.csv')