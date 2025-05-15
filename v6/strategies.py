INITIAL_VALUE = 10 ** 9
STATEGIES = {
    'ever': lambda r, n, i: True,
    'never': lambda r, n, i: False,
    
    'raised[i]': lambda r, n, i: r[i],
    'not raised[i]': lambda r, n, i: not r[i],

    'raised[i] or raised[i-1]': lambda r, n, i: r[i] or r[i-1],
    'not (raised[i] or raised[i-1])': lambda r, n, i: not (r[i] or r[i-1]),

    'raised[i] and raised[i-1]': lambda r, n, i: r[i] and r[i-1],
    'not (raised[i] and raised[i-1])': lambda r, n, i: not (r[i] and r[i-1]),

    'raised[i] and not raised[i-1]': lambda r, n, i: r[i] and not r[i-1],
    'not (raised[i] and not raised[i-1])': lambda r, n, i: not (r[i] and not r[i-1]),

    'raised[i] or not raised[i-1]': lambda r, n, i: r[i] or not r[i-1],
    'not (raised[i] or not raised[i-1])': lambda r, n, i: not (r[i] or not r[i-1]),

    # !A && !B == !(A || B)
    # 'not raised[i] and not raised[i-1]': lambda r, n, i: not r[i] and not r[i-1],
    # !(!A && !B) == (A || B)
    # 'not (not raised[i] and not raised[i-1])': lambda r, n, i: not (not r[i] and not r[i-1]),

    # !A || !B == !(A && B)
    # 'not raised[i] or not raised[i-1]': lambda r, n, i: not r[i] or not r[i-1],
    # !(!A || !B) == (A && B)
    # 'not (not raised[i] or not raised[i-1])': lambda r, n, i: not (not r[i] or not r[i-1]),

    'next[i]': lambda r, n, i: n[i]
}


def do_stategies(data):
    closes, raiseds, nexts = data['Close'].tolist(), data['Raised'].tolist(), data['Next Raised'].tolist()

    result = {}

    for name, condition in STATEGIES.items():
        montante = INITIAL_VALUE
        values = [montante]
        num_acoes = 0
        for i in range(1, len(closes)):
            if condition(raiseds, nexts, i):
                # compra ações
                num_acoes += montante // closes[i]
                montante %= closes[i]
            else:
                # vende ações
                montante += closes[i] * num_acoes
                num_acoes = 0
            values.append(float(montante + closes[i] * num_acoes))
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