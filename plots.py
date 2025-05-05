import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates # Para formatar as datas no eixo X

def plot_last_closings(data, ticker_name, period):
    sns.set_theme()
    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Gráfico 1: Preço de Fechamento
    ax[0].plot(data.index, data['Close'], label='Preço de Fechamento', color='blue')

    # plotagem da média móvel de 7 dias
    ax[0].plot(data.index, data['MM_7'], label='Média Móvel 7 dias', color='orange', linestyle='--')

    # plotagem da média móvel de 15 dias
    ax[0].plot(data.index, data['MM_15'], label='Média Móvel 7 dias', color='black', linestyle='--')

    ax[0].set_ylabel('Preço (R$)')
    ax[0].set_title(f'Histórico de Preços - {ticker_name} ({period})')
    ax[0].legend()
    ax[0].grid(True)

    # Gráfico 2: Variação Diária Percentual
    # Usaremos barras para melhor visualização das variações diárias
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