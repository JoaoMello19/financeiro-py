import numpy as np
import yfinance as yf


def get_ticker_info(ticker_name, period="1mo", verbose=False):
    if verbose:
        print(f"Bucando dados para {ticker_name} no período {period}...")

    ticker = yf.Ticker(ticker_name)
    data = ticker.history(period=period)[['Open', 'High', 'Low', 'Close', 'Volume']]

    if data.empty:
        if verbose:
            print(f"Não foi possível obter dados para {ticker_name}...")
        return None

    # adicionando algumas colunas uteis
    data["% Change"] = data["Close"].pct_change() * 100

    data['MM_7']     = data['Close'].rolling(window=7).mean()
    data['MM_15']    = data['Close'].rolling(window=15).mean()
    data['Delta_MM'] = data['MM_7'] - data["MM_15"]

    data['Raised'] = np.where(data["% Change"] > 0, 1, 0)
    data['Next Raised'] = data['Raised'].shift(-1)

    if verbose:
        print("Dados dos últimos 5 dias:", data[["Close", "% Change"]].tail(), sep="\n")

    return data.dropna()


if __name__ == "__main__":
    get_ticker_info("MGLU3.SA", verbose=True)