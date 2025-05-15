import json
import models
import plots
import tickers


TICKERS = ["AAPL", "PETR4.SA", "IVVB11.SA", "VALE3.SA", "BTC-USD"]
RESULTS = {}

for ticker in TICKERS:
    data = tickers.get_ticker_data(ticker)

    # gráficos sobre os dados
    plots.plot_last_closings(data, ticker)
    plots.plot_covariance(data, ticker)

    # pré-processando
    data = models.preprocess(data)
    X_train, X_test, y_train, y_test = models.train_test_split(data)

    RESULTS[ticker] = {
        "SVM": models.do_svm(X_train, X_test, y_train, y_test),
        "MLP": models.do_mlp(X_train, X_test, y_train, y_test),
        "RANDOM FOREST": models.do_random_forest(X_train, X_test, y_train, y_test),
        "XGBOOST": models.do_xgboost(X_train, X_test, y_train, y_test)
    }

with open('results.json', 'w') as f:
    json.dump(RESULTS, f, indent=4)