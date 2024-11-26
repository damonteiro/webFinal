import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sqlalchemy import create_engine

# Conecta com o banco de dados SQLite
engine = create_engine('sqlite:///banco.db', echo=True)

df_lido = pd.read_sql('SELECT * FROM dados', con=engine)

# Opções para análise estatística
tipos_analise = ['Valor da Média', 'Valor da Mediana', 'Desvio Padrão']
st.sidebar.header('Tipo de análise estatística:')
estatistica_escolhida = st.sidebar.selectbox('Selecione o tipo de análise', tipos_analise)

# Calcular estatísticas básicas
if estatistica_escolhida == 'Valor da Média':
    media = df_lido['preco'].mean()
    st.sidebar.header("Estatísticas:")
    st.sidebar.write(f"O valor de Média dos preços de todos os notebooks: R$ {media:.2f}")
elif estatistica_escolhida == 'Valor da Mediana':
    mediana = df_lido['preco'].median()
    st.sidebar.header("Estatísticas:")
    st.sidebar.write(f"O valor de Mediana dos preços de todos os notebooks: R$ {mediana:.2f}")
elif estatistica_escolhida == 'Desvio Padrão':
    desvio_padrao = df_lido['preco'].std()
    st.sidebar.header("Estatísticas:")
    st.sidebar.write(f"O Desvio Padrão dos preços de todos os notebooks: R$ {desvio_padrao:.2f}")

# Gráficos
graficos = ['Gráficos Univariados', 'Gráficos Multivariados']
st.sidebar.header('Gráficos:')
tipo_grafico = st.sidebar.selectbox('Selecione um tipo de análise gráfica', graficos)

st.subheader("Gráficos e Visualizações")

# Gráficos Univariados
if tipo_grafico == 'Gráficos Univariados':
    expander1 = st.expander('Sessão Gráficos Univariados')

    with expander1:
        fig, axs = plt.subplots(2, 2, figsize=(12, 12))  # Organizando em 2x2 (2 em cima e 2 embaixo)

        # Primeiro gráfico: Histograma
        axs[0, 0].hist(df_lido['preco'], bins=10, color='blue', alpha=0.7)
        axs[0, 0].set_title("Histograma de Preços de Notebooks", fontsize=16)
        axs[0, 0].set_xlabel("Preço (R$)", fontsize=14)
        axs[0, 0].set_ylabel("Frequência", fontsize=14)

        # Segundo gráfico: Boxplot
        sns.boxplot(x=df_lido['preco'], ax=axs[0, 1], linewidth=2)
        axs[0, 1].set_title("Boxplot de Preços de Notebooks", fontsize=16)

        # Terceiro gráfico: Contagem de Notebooks
        notebook_counts = df_lido['notebook'].value_counts()
        axs[1, 0].bar(notebook_counts.index, notebook_counts.values, color='green', linewidth=2, edgecolor='black')
        axs[1, 0].set_title("Contagem de Notebooks", fontsize=16)
        axs[1, 0].set_xlabel("Nome do Notebook", fontsize=14)
        axs[1, 0].set_ylabel("Contagem", fontsize=14)
        axs[1, 0].tick_params(axis='x', rotation=45) # Inclina os rótulos para facilitar leitura

        # Quarto gráfico: Gráfico de Pizza (distribuição de preços)
        preço_por_notebook = df_lido.groupby('notebook')['preco'].sum()
        axs[1, 1].pie(preço_por_notebook, labels=preço_por_notebook.index, autopct='%1.1f%%', startangle=90)
        axs[1, 1].set_title("Distribuição Percentual dos Preços dos Notebooks", fontsize=16)

        # Exibindo no Streamlit
        st.pyplot(fig)

# Gráficos Multivariados
elif tipo_grafico == 'Gráficos Multivariados':
    expander2 = st.expander('Sessão Gráficos Multivariados')

    with expander2:
        fig2, axs2 = plt.subplots(2, 2, figsize=(15, 12))

        # Gráfico de Dispersão
        sns.scatterplot(
            x=df_lido['preco'],  # Preço no eixo X
            y=df_lido['tamanho_tela'],  # Tamanho da tela no eixo Y
            hue=df_lido['notebook'],  # Diferenciação por nome do notebook
            palette="viridis",  # Paleta de cores
            s=100,  # Tamanho dos pontos
            ax=axs2[0, 0]
        )
        axs2[0, 0].set_title("Relação entre Preço e Tamanho da Tela", fontsize=16)

        # Gráfico de Boxplot (Preço por Notebook)
        sns.boxplot(x='notebook', y='preco', data=df_lido, ax=axs2[0, 1])
        axs2[0, 1].set_title("Preço por Notebook", fontsize=16)

        # Gráfico de Barras (Preço médio por Notebook)
        preço_medio_por_notebook = df_lido.groupby('notebook')['preco'].mean()
        sns.barplot(x=preço_medio_por_notebook.index, y=preço_medio_por_notebook.values, ax=axs2[1, 0])
        axs2[1, 0].set_title("Preço Médio por Notebook", fontsize=16)

        # Gráfico de Histograma (Preço por Notebook)
        sns.histplot(df_lido['preco'], kde=True, color='purple', ax=axs2[1, 1])
        axs2[1, 1].set_title("Histograma dos Preços", fontsize=16)

        # Exibindo no Streamlit
        st.pyplot(fig2)
        st.write("Gráficos multivariados: relação entre preço, tamanho da tela e diferentes notebooks.")
