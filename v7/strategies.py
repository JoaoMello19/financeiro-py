INITIAL_VALUE = 10 ** 9
STATEGIES = {
    'ever': lambda today: True,
    'never': lambda today: False,
    
    'raised': lambda today: today['Raised'],
    'not raised': lambda today: not today['Raised'],

    'raised or lagR_1': lambda today: today['Raised'] or today['LagR_1'],
    'not (raised or lagR_1)': lambda today: not (today['Raised'] or today['LagR_1']),

    'raised and lagR_1': lambda today: today['Raised'] and today['LagR_1'],
    'not (raised and lagR_1)': lambda today: not (today['Raised'] and today['LagR_1']),

    'raised and not lagR_1': lambda today: today['Raised'] and not today['LagR_1'],
    'not (raised and not lagR_1)': lambda today: not (today['Raised'] and not today['LagR_1']),

    'raised or not lagR_1': lambda today: today['Raised'] or not today['LagR_1'],
    'not (raised or not lagR_1)': lambda today: not (today['Raised'] or not today['LagR_1']),

    'next_raised': lambda today: today['Next Raised'],
}


def do_stategies(data):
    result = {}

    for name, condition in STATEGIES.items():
        montante = INITIAL_VALUE
        values = [montante]
        num_acoes = 0
        for i in range(len(data)):
            today = data.iloc[i]
            if condition(today):
                # compra ações
                num_acoes += montante // today['Close']
                montante %= today['Close']
            else:
                # vende ações
                montante += today['Close'] * num_acoes
                num_acoes = 0
            values.append(float(montante + today['Close'] * num_acoes))
        result[name] = values

    return result


def evaluate_strategies(values):
    result = {}
    for strategie in STATEGIES.keys():
        values_s = values[strategie]
        result[strategie] = {
            'inicio': values_s[0],
            'minimo': min(values_s),
            'maximo': max(values_s),
            'final': values_s[-1],
            'variacao': values_s[-1] - values_s[0],
            'variacao%': ((values_s[-1] / values_s[0]) - 1) * 100,
        }
    return result