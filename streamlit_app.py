import streamlit as st
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go



# Defina o título da página
st.set_page_config(page_title='Minha Dashboard Interativa', layout='wide')

# Defina a função importar_dados
@st.cache_data
def importar_dados():
    # Use o caminho do arquivo fornecido
    caminho_arquivo_csv = (r"Criptomoedas.csv")
    # Importar o arquivo CSV para um DataFrame
    df = pd.read_csv(caminho_arquivo_csv)
    return df.copy()

# Crie um cabeçalho e uma barra lateral
st.title('Análises de Cripto Moedas')
st.sidebar.header('Menu')

# Adicione opções ao menu da barra lateral
opcoes = ['Home','Visualização','Análise', 'Sobre']
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

# Carregue os dados uma vez para uso posterior
df = importar_dados()

# Crie páginas diferentes com base na escolha do usuário
if escolha == 'Home':
    url_da_imagem = 'https://images.unsplash.com/photo-1516245834210-c4c142787335?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    st.image(url_da_imagem, use_column_width=True)

    st.subheader('Bem-vindo à página inicial!')
    st.write('Aqui você pode encontrar informações valiosas sobre Criptomoedas.')

elif escolha == 'Análise':
    st.subheader('Análise de Dados')

    # Adicionar a explicação do objetivo da análise
    st.write("""
    # Objetivo da Análise

    O objetivo desta análise é fornecer insights valiosos sobre o desempenho das respectivas  criptomoedas. Ao calcular o retorno diário e a volatilidade (uma medida de risco) para cada criptomoeda, podemos avaliar o desempenho passado e a estabilidade de cada moeda.

    Além disso, ao visualizar esses dados em um gráfico de dispersão, podemos comparar facilmente o risco e o retorno de diferentes criptomoedas. Isso pode ajudar os investidores a tomar decisões informadas sobre quais criptomoedas podem ser um bom investimento, com base em seu apetite por risco e suas expectativas de retorno.

    Por fim, ao visualizar a volatilidade de cada moeda em um gráfico de barras, podemos ver rapidamente quais moedas são as mais voláteis. Isso pode ser útil para os investidores que estão interessados em negociar ativamente criptomoedas, pois as moedas voláteis podem oferecer mais oportunidades para lucros de curto prazo.
    """)

    st.write("Primeiras linhas do DataFrame:")
    st.dataframe(df.head())

    volatilities = []
    moedas = []
    for moeda in df['moeda'].unique():
        df_moeda = df[df['moeda'] == moeda].copy()
        df_moeda['retorno'] = df_moeda['fechamento'].pct_change()
        volatility = df_moeda['retorno'].std()
        volatilities.append(volatility)
        moedas.append(moeda)

    df_volatilidades = pd.DataFrame({'Moeda': moedas, 'Volatilidade': volatilities})

    fig = px.bar(df_volatilidades, x='Moeda', y='Volatilidade', labels={'Volatilidade': 'Volatilidade', 'Moeda': 'Moeda'})
    fig.update_layout(title='Volatilidade percentual de cada moeda', xaxis_title='Moeda', yaxis_title='Volatilidade')
    st.plotly_chart(fig)


elif escolha == 'Visualização':
    st.subheader('Visualização de Dados')

    data_inicio = datetime.now() - timedelta(days=30)
    df['tempo'] = pd.to_datetime(df['tempo'])
    df_ultimos_30_dias = df[df['tempo'] >= data_inicio]

    df_ultimos_30_dias = df_ultimos_30_dias.reset_index()
    df_ultimos_30_dias['var_percentual'] = df_ultimos_30_dias.groupby('moeda')['fechamento'].pct_change()

    fig = px.line(df_ultimos_30_dias, x='tempo', y='var_percentual', color='moeda', labels={'var_percentual': 'Variação Percentual'})
    fig.update_layout(title='Variação Percentual nos Últimos 30 Dias', xaxis_title='Tempo', yaxis_title='Variação Percentual')
    st.plotly_chart(fig)

elif escolha == 'Sobre':
    st.subheader('Sobre esta Dashboard')
    st.write("""
# Dashboard Interativa de Análise de Criptomoedas

Bem-vindo à nossa dashboard interativa de análise de criptomoedas! Aqui, você encontrará insights valiosos e análises detalhadas que podem ajudar a orientar suas decisões de investimento em criptomoedas.

Com esta ferramenta, você pode:

- Explorar tendências e padrões no mercado de criptomoedas.
- Analisar o desempenho passado de várias criptomoedas.
- Avaliar o risco e o retorno potencial de diferentes criptomoedas.

Lembre-se, enquanto esta ferramenta fornece informações úteis, é importante fazer sua própria pesquisa e consultar um consultor financeiro antes de tomar decisões de investimento.
""")

 # Função para buscar dados da criptomoeda selecionada
def fetch_crypto_data(df, moeda):
    # Filtra o DataFrame para incluir apenas os dados da moeda desejada
    df_selected_crypto = df[df['moeda'] == moeda].copy()
    
    # Calcula os retornos diários
    df_selected_crypto['Retornos Diários (%)'] = df_selected_crypto['fechamento'].pct_change() * 100
    
    return df_selected_crypto


# Lista das criptomoedas que você quer importar
criptomoedas = ['BTC', 'ETH', 'ADA', 'BNB']

# Loop através de cada criptomoeda
for cripto in criptomoedas:
    # Chame a função para obter os dados da criptomoeda selecionada
    df_selected_crypto = fetch_crypto_data(df, cripto)


    if escolha == 'Visualização':
        # Cria um gráfico de barras para visualizar os retornos diários em porcentagem
        fig = px.bar(df_selected_crypto, x='tempo', y='Retornos Diários (%)', 
                     labels={'Retornos Diários (%)': 'Variação Percentual', 'tempo': 'Data'},
                     title=f'Variação Percentual Diária - Último Mês - {cripto}')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

        # Cria um gráfico de série temporal para visualizar os retornos diários em porcentagem
        fig = px.line(df_selected_crypto, x='tempo', y='fechamento', 
                      labels={'close': 'Preço de Fechamento', 'tempo': 'Data'},
                      title=f'Preço de Fechamento ao Longo do Tempo - {cripto}')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

import altair as alt
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import streamlit as st

df_BTC = df[df['moeda'] == 'BTC']
df_ETH = df[df['moeda'] == 'ETH']
df_ADA = df[df['moeda'] == 'ADA']
df_BNB = df[df['moeda'] == 'BNB']

# Calcular o retorno diário para BTC
df_BTC['retorno_diario'] = df_BTC['fechamento'].pct_change()

# Calcular o retorno diário para ETH
df_ETH['retorno_diario'] = df_ETH['fechamento'].pct_change()

# Calcular o retorno diário para BNB
df_BNB['retorno_diario'] = df_BNB['fechamento'].pct_change()

# Calcular o retorno diário para ADA
df_ADA['retorno_diario'] = df_ADA['fechamento'].pct_change()

if escolha == 'Análise':
    st.subheader('Abaixo segue o gráfico de probabilidade de variação de preço para cada moeda')


    df_BTC = df[df['moeda'] == 'BTC']
    df_ETH = df[df['moeda'] == 'ETH']
    df_ADA = df[df['moeda'] == 'ADA']
    df_BNB = df[df['moeda'] == 'BNB']

    # Calcular o retorno diário para BTC
    df_BTC['retorno_diario'] = df_BTC['fechamento'].pct_change()

    # Calcular o retorno diário para ETH
    df_ETH['retorno_diario'] = df_ETH['fechamento'].pct_change()

    # Calcular o retorno diário para BNB
    df_BNB['retorno_diario'] = df_BNB['fechamento'].pct_change()

    # Calcular o retorno diário para ADA
    df_ADA['retorno_diario'] = df_ADA['fechamento'].pct_change()

    # Suponha que dfs seja uma lista de dataframes para BTC, ETH, ADA, BNB
    dfs = [df_BTC, df_ETH, df_ADA, df_BNB]
    labels = ['BTC', 'ETH', 'ADA', 'BNB']

    # Loop através de cada dataframe
    for i, (df, label) in enumerate(zip(dfs, labels)):
        # Remover valores NaN
        df = df.dropna()

        # Ajustar uma distribuição normal à distribuição de dados
        mu, std = norm.fit(df['retorno_diario'])
        x = np.linspace(df['retorno_diario'].min(), df['retorno_diario'].max(), 100)
        p = norm.pdf(x, mu, std)

        # Criar um dataframe para a curva normal
        df_normal = pd.DataFrame({'x': x, 'p': p})

        # Criar o gráfico de histograma
        histogram = alt.Chart(df).transform_density(
            'retorno_diario',
            as_=['retorno_diario', 'density'],
            extent=[df['retorno_diario'].min(), df['retorno_diario'].max()]
        ).mark_area(opacity=0.5).encode(
            alt.X('retorno_diario:Q'),
            alt.Y('density:Q'),
        )

        # Criar o gráfico da curva normal
        normal_curve = alt.Chart(df_normal).mark_line(color='red').encode(
            alt.X('x'),
            alt.Y('p')
        )

        # Adicionar um título ao gráfico
        st.write(f'## {label}')

        # Exibir o gráfico
        st.altair_chart(histogram + normal_curve)

        # Adicione seu novo código aqui:
        st.write(f"{label} - Retorno Médio: {df['retorno_diario'].mean()}, Risco: {df['retorno_diario'].std()}")

    # Criar um gráfico de dispersão interativo com Plotly
    fig = go.Figure()

    # Adicionar os pontos ao gráfico
    fig.add_trace(go.Scatter(x=[df_BTC['retorno_diario'].mean()], y=[df_BTC['retorno_diario'].std()], mode='markers', name='BTC'))
    fig.add_trace(go.Scatter(x=[df_ETH['retorno_diario'].mean()], y=[df_ETH['retorno_diario'].std()], mode='markers', name='ETH'))
    fig.add_trace(go.Scatter(x=[df_BNB['retorno_diario'].mean()], y=[df_BNB['retorno_diario'].std()], mode='markers', name='BNB'))
    fig.add_trace(go.Scatter(x=[df_ADA['retorno_diario'].mean()], y=[df_ADA['retorno_diario'].std()], mode='markers', name='ADA'))

    # Configurar os eixos e a grade
    fig.update_xaxes(title='Média esperada retorno diário', showgrid=True)
    fig.update_yaxes(title='Risco diário', showgrid=True)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

if escolha == 'Análise':
    st.subheader('Gráfico de risco Retorno')

    # Incluir a explicação detalhada aqui
    st.write("""
    # Análise de Risco-Retorno

    A análise de risco-retorno é uma técnica fundamental na gestão de investimentos. Ela envolve a avaliação quantitativa do retorno esperado de um investimento e do risco associado a ele.

    ## Retorno

    O retorno de um investimento é a mudança no valor do investimento ao longo de um período de tempo, que pode ser expressa como uma porcentagem do valor inicial do investimento. No nosso caso, estamos calculando o retorno diário, que é a variação percentual no preço de fechamento de um dia para o outro.

    ## Risco

    O risco de um investimento é uma medida da incerteza ou volatilidade dos seus retornos. Uma maneira comum de medir o risco é usar o desvio padrão dos retornos, que é uma medida de quão dispersos estão os retornos em relação à média. Estamos calculando o risco como o desvio padrão do retorno diário.

    ## Gráfico de Risco-Retorno

    Estamos criando um gráfico de dispersão que mostra o risco (no eixo y) versus o retorno (no eixo x) para cada criptomoeda. Cada ponto no gráfico representa uma criptomoeda. Isso permite que você compare visualmente o risco e o retorno de diferentes criptomoedas.

    Em geral, os investidores preferem investimentos com altos retornos e baixos riscos. No entanto, na prática, investimentos com retornos potencialmente mais altos geralmente vêm com um risco maior. Portanto, a análise de risco-retorno é uma ferramenta importante para ajudar os investidores a tomar decisões informadas sobre onde colocar seu dinheiro.
    """)

    x = ['BTC', 'ETH', 'BNB', 'ADA']
    retorno_medio = [df_BTC['retorno_diario'].mean(), df_ETH['retorno_diario'].mean(), df_BNB['retorno_diario'].mean(), df_ADA['retorno_diario'].mean()]
    risco = [df_BTC['retorno_diario'].std(), df_ETH['retorno_diario'].std(), df_BNB['retorno_diario'].std(), df_ADA['retorno_diario'].std()]

    fig, ax = plt.subplots()
    ax.bar(x, retorno_medio)

    ax2 = ax.twinx()
    ax2.plot(x, risco, color='red')

    ax.set_xlabel('Criptomoedas')
    ax.set_ylabel('Retorno Médio')
    ax2.set_ylabel('Risco')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)

    # Adicione seu novo código aqui:
    st.write(f"BTC - Retorno Médio: {df_BTC['retorno_diario'].mean()}, Risco: {df_BTC['retorno_diario'].std()}")
    st.write(f"ETH - Retorno Médio: {df_ETH['retorno_diario'].mean()}, Risco: {df_ETH['retorno_diario'].std()}")
    st.write(f"BNB - Retorno Médio: {df_BNB['retorno_diario'].mean()}, Risco: {df_BNB['retorno_diario'].std()}")
    st.write(f"ADA - Retorno Médio: {df_ADA['retorno_diario'].mean()}, Risco: {df_ADA['retorno_diario'].std()}")
