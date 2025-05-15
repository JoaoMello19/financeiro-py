import plots
import tickers


TICKERS = ["AAPL", "PETR4.SA", "IVVB11.SA", "VALE3.SA", "BTC-USD"]
RESULTS = {}

for ticker in TICKERS:
    data = tickers.get_ticker_data(ticker)

    plots.plot_last_closings(data, ticker)
    plots.plot_covariance(data, ticker)