import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates # Para formatar as datas no eixo X

def plot_last_closings(data, ticker_name, period):
    sns.set_theme()
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    data = data.dropna(subset=['MM_7', 'MM_15'])

    # Gráfico 1: Preço de Fechamento
    # Usa scatter para colorir os pontos com base nas médias móveis
    ax[0].plot(data.index, data['Close'], label='Preço de Fechamento', color='blue')

    # plotagem da média móvel de 7/15 dias
    ax[0].plot(data.index, data['MM_7'], label='Média Móvel 7 dias', color='orange', linestyle='--')
    ax[0].plot(data.index, data['MM_15'], label='Média Móvel 15 dias', color='purple', linestyle='--')

    ax[0].set_ylabel('Preço (R$)')
    ax[0].set_title(f'Histórico de Preços - {ticker_name} ({period})')
    ax[0].legend()
    ax[0].grid(True)

    # Gráfico 2: Variação Diária Percentual
    cores = ['green' if x > 0 else 'red' for x in data['% Change'].fillna(0)] # Verde para positivo, Vermelho para negativo
    ax[1].bar(data.index, data['% Change'], label='Variação Diária (%)', color=cores, width=0.8)
    ax[1].axhline(0, color='black', linestyle='--', linewidth=0.7) # Linha no zero para referência
    ax[1].set_ylabel('Variação (%)')
    ax[1].set_title(f'Variação Diária Percentual - {ticker_name} ({period})')
    ax[1].legend()
    ax[1].grid(True)

    # Melhorar a formatação do eixo X (datas)
    ax[1].xaxis.set_major_locator(mdates.AutoDateLocator()) # Escolhe os melhores locais para os ticks de data
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # Formato da data
    plt.xlabel('Data') # Rótulo do eixo X comum aos dois gráficos
    plt.xticks(rotation=45) # Rotaciona os rótulos das datas para não sobrepor

    plt.tight_layout() # Ajusta o layout para evitar sobreposição de títulos/rótulos
    plt.savefig(f'./graficos/{ticker_name}.png')