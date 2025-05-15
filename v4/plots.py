import matplotlib.dates as mdates # Para formatar as datas no eixo X
import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme()
FILE_PATH = "./graficos/"

def plot_last_closings(data, ticker_name, period="1y"):
    def add_graph1(ax):
        # Gráfico 1: Preço de Fechamento
        # Usa scatter para colorir os pontos com base nas médias móveis
        ax.plot(data.index, data['Close'], label='Preço de Fechamento', color='blue')

        # plotagem da média móvel de 7/15 dias
        ax.plot(data.index, data['MM_15'], label='Média Móvel 15 dias', color='purple', linestyle='--')

        ax.set_ylabel('Preço (R$)')
        ax.set_title(f'Histórico de Preços - {ticker_name} ({period})')
        ax.legend()
        ax.grid(True)
    
    def add_graph2(ax):
        # Gráfico 2: Variação Diária Percentual
        cores = ['green' if x > 0 else 'red' for x in data['% Change'].fillna(0)] # Verde para positivo, Vermelho para negativo
        ax.bar(data.index, data['% Change'], label='Variação Diária (%)', color=cores, width=0.8)
        ax.axhline(0, color='black', linestyle='--', linewidth=0.7) # Linha no zero para referência
        ax.set_ylabel('Variação (%)')
        ax.set_title(f'Variação Diária Percentual - {ticker_name} ({period})')
        ax.legend()
        ax.grid(True)

    fig, ax = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    add_graph1(ax[0])
    add_graph2(ax[1])

    # Melhorar a formatação do eixo X (datas)
    ax[1].xaxis.set_major_locator(mdates.AutoDateLocator()) # Escolhe os melhores locais para os ticks de data
    ax[1].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d')) # Formato da data
    plt.xlabel('Data') # Rótulo do eixo X comum aos dois gráficos
    plt.xticks(rotation=45) # Rotaciona os rótulos das datas para não sobrepor

    plt.tight_layout() # Ajusta o layout para evitar sobreposição de títulos/rótulos
    plt.savefig(f'./graficos/data_{ticker_name}.png')
    plt.close()


def plot_covariance(data, ticker):
    # Considera apenas colunas numéricas e remove linhas com NaN
    corr = data.select_dtypes(include="number").corr()

    # Gera e salva o heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True,
        annot_kws={"size": 8},  # Define o tamanho da fonte dos números
        cmap="coolwarm",
        fmt=".1f",
        square=True
    )
    plt.title(f"Mapa de Calor - Correlação de {ticker}")
    plt.tight_layout()
    
    # Caminho do arquivo
    filename = f"heatmap_{ticker.replace('.', '_')}.png"
    plt.savefig(FILE_PATH + filename)
    plt.close()  # Fecha a figura para evitar sobreposição na próxima
    pass