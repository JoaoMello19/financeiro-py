import tickers
import plots


TICKER_NAME = "MGLU3.SA"
PERIOD = "1y"

data = tickers.get_ticker_info(TICKER_NAME, PERIOD)
plots.plot_last_closings(data, TICKER_NAME, PERIOD)
