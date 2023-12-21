import streamlit as st
import ccxt
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Defina o título da página
st.set_page_config(page_title='Minha Dashboard Interativa', layout='wide')

# Defina a função importar_dados
@st.cache_data
def importar_dados():
    # Use o caminho do arquivo fornecido
     caminho_arquivo_csv = 'Criptomoedadas.csv'
    # Importar o arquivo CSV para um DataFrame
    df = pd.read_csv(caminho_arquivo_csv)
    return df.copy()

# Crie um cabeçalho e uma barra lateral
st.title('Análises de Cripto Moedas')
st.sidebar.header('Menu')

# Adicione opções ao menu da barra lateral
opcoes = ['Home', 'Análise', 'Visualização', 'Sobre']
escolha = st.sidebar.selectbox("Escolha uma opção", opcoes)

# Carregue os dados uma vez para uso posterior
df = importar_dados()

# Crie páginas diferentes com base na escolha do usuário
if escolha == 'Home':
    url_da_imagem = 'https://images.unsplash.com/photo-1516245834210-c4c142787335?q=80&w=1469&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    st.image(url_da_imagem, use_column_width=True)

    st.subheader('Bem-vindo à página inicial!')
    st.write('Aqui você pode encontrar informações gerais sobre Criptomoedas.')

elif escolha == 'Análise':
    st.subheader('Análise de Dados')

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
    fig.update_layout(title='Volatilidade por Moeda', xaxis_title='Moeda', yaxis_title='Volatilidade')
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
    st.write('Esta é uma dashboard interativa para análise de criptomoedas.')

 # Função para buscar dados da criptomoeda selecionada
def fetch_crypto_data(symbol):
    exchange = ccxt.binance()
    data = exchange.fetch_ohlcv(f'{symbol}/USDT', '1d')
    df = pd.DataFrame(data, columns=['tempo', 'open', 'high', 'low', 'close', 'volume'])
    df['tempo'] = pd.to_datetime(df['tempo'], unit='ms')
    df['Retornos Diários (%)'] = df['close'].pct_change() * 100
    return df

# Lista das criptomoedas que você quer importar
criptomoedas = ['BTC', 'ETH', 'ADA', 'BNB']

# Loop através de cada criptomoeda
for cripto in criptomoedas:
    # Chame a função para obter os dados da criptomoeda selecionada
    df_selected_crypto = fetch_crypto_data(cripto)

    if escolha == 'Visualização':
        # Cria um gráfico de barras para visualizar os retornos diários em porcentagem
        fig = px.bar(df_selected_crypto, x='tempo', y='Retornos Diários (%)', 
                     labels={'Retornos Diários (%)': 'Variação Percentual', 'tempo': 'Data'},
                     title=f'Variação Percentual Diária - Último Mês - {cripto}')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

        # Cria um gráfico de série temporal para visualizar os retornos diários em porcentagem
        fig = px.line(df_selected_crypto, x='tempo', y='close', 
                      labels={'close': 'Preço de Fechamento', 'tempo': 'Data'},
                      title=f'Preço de Fechamento ao Longo do Tempo - {cripto}')
        # Exibir o gráfico no Streamlit
        st.plotly_chart(fig)

if escolha == 'Análise':
    st.subheader('Visualização de Dados')

    # Seu código existente aqui...

    # Adicione seu novo código aqui:
    import altair as alt
    import numpy as np
    from scipy.stats import norm

    df_BTC = df[df['moeda'] == 'BTC']
    df_ETH = df[df['moeda'] == 'ETH']
    df_ADA = df[df['moeda'] == 'ADA']
    df_BNB = df[df['moeda'] == 'BNB']

    # Suponha que dfs seja uma lista de dataframes para BTC, ETH, ADA, BNB
    dfs = [df_BTC, df_ETH, df_ADA, df_BNB]
    labels = ['BTC', 'ETH', 'ADA', 'BNB']

    # Loop através de cada dataframe
    for i, (df, label) in enumerate(zip(dfs, labels)):
        # Calcular o retorno diário
        df['retorno_diario'] = df['fechamento'].pct_change()

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
