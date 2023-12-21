import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

# Defina o título da página
st.set_page_config(page_title='Minha Dashboard Interativa', layout='wide')

# Defina a função importar_dados
@st.cache_data
def importar_dados():
    # Use o caminho do arquivo fornecido
    caminho_arquivo_csv = 'Criptomoedas.csv'

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
    st.write('Aqui você pode encontrar as principais informações sobre Criptomoedas.')

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
    fig.update_layout(title='Volatilidade percentual por  Moeda', xaxis_title='Moeda', yaxis_title='Volatilidade')
    st.plotly_chart(fig)

elif escolha == 'Visualização':
    st.subheader('Visualização de Dados')

    st.write("# Histograma de Probabilidade de Retorno:")

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

    import plotly.graph_objects as go

    # Suponha que dfs seja uma lista de dataframes para BTC, ETH, ADA, BNB
    dfs = [df_BTC, df_ETH, df_ADA, df_BNB]
    labels = ['BTC', 'ETH', 'ADA', 'BNB']

    # Loop através de cada dataframe
    for i, (df, label) in enumerate(zip(dfs, labels)):
        # Criar o gráfico de série temporal
        fig = go.Figure(data=[go.Scatter(
            x=df['tempo'],
            y=df['fechamento'],
            mode='lines',
            name=label
        )])

        # Adicionar títulos
        fig.update_layout(title=f'Série Temporal para {label}',
                          xaxis_title='Tempo',
                          yaxis_title='Fechamento')

        # Exibir o gráfico
        st.plotly_chart(fig)
