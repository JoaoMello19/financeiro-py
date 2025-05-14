# Sistema de Análise de Ativos Financeiros

# Obtenção dos dados

Os dados sobre os ativos são recuperados do Yahoo Finance (https://finance.yahoo.com/) através do pacote **yfinance**.

# Análises dos dados brutos

Os dados coletados são filtrados e apenas algumas colunas são mantidas para a análise:

## Open, High, Low e Close

Colunas que indicam os valores de abertura, máximo, mínimo e de fechamento de um ativo, respecivamente.
O tipo dos dados é decimal (**float64**) e não apresentam, para a maioria dos casos a serem analisados, _outliers_ significativos, mantendo a mesma escala de valores.

## Volume

Representa o volume de movimentações relativas a esse ativo.
O tipo dessa coluna é inteiro (**int64**), com dados variando significativamente é grandes outliers.

# Criação de novas colunas

## % Change

Representa a porcentagem de mudanças de um dia em relação ao outro.
- se **menor que 0**, houve queda;
- se **igual a 0**, houve estabilidade;
- se **maior que 0**, houve subida.

## MM_7 e MM_15

Médias móveis de **7 e 15 dias**, respectivamente, referente a coluna **"Close"**.
Estão na mesma escala e com o mesmo tipo de dados da coluna mencionada.

# Estratégias de Pré-Processamento
