import json
import os
import pandas as pd
import strategies as strat
import tickers


TICKERS = ["AAPL", "PETR4.SA", "IVVB11.SA", "VALE3.SA", "BTC-USD", "ABEV3.SA"]
PERIOD = "max"
RESULTS = {}
VARIATIONS = {}

for ticker in TICKERS:
    # usa a API apenas quando os dados nao estao salvos
    if os.path.exists(f'./csv/{ticker}_{PERIOD}.csv'):
        data = pd.read_csv(f'./csv/{ticker}_{PERIOD}.csv', index_col=0)
    else:
        data = tickers.get_ticker_data(ticker, PERIOD)
        data.to_csv(f'./csv/{ticker}_{PERIOD}.csv')
    
    # aplica cada estratégia nos dados
    values = strat.do_stategies(data)
    # avalia cada estratégia
    RESULTS[ticker] = strat.evaluate_strategies(values)

# filtra apenas as variações de cada estratégia
for ticker, data in RESULTS.items():
    VARIATIONS[ticker] = {}
    for strategy, info in data.items():
        VARIATIONS[ticker][strategy] = info['variacao%']

# salva os resultados
pd.DataFrame(RESULTS).to_csv('./csv/strategies.csv')
with open('results.json', 'w') as f:
    json.dump(RESULTS, f, indent=4)

df_vars = pd.DataFrame(VARIATIONS)
df_vars['means'] = df_vars.mean(axis=1)
df_vars.sort_values(by='means', ascending=False, inplace=True)
print(df_vars)