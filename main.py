import tickers
import plots


TICKER_NAME = "BTC-USD"
PERIOD = "max"

data = tickers.get_ticker_info(TICKER_NAME, PERIOD)
plots.plot_last_closings(data, TICKER_NAME, PERIOD)

# print(data.tail(10))