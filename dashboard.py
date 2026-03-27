import streamlit as st
import pandas as pd
import plotly.express as px 
import ast

st.set_page_config(page_title="Cinescópio", page_icon="icon.jpg", layout="wide")

df = pd.read_csv('movies.csv', sep=',', decimal='.')

year = st.sidebar.selectbox('Selecione o ano', df.release_year.unique())

df.year = df[df['release_year'] == year] 




st.header(f"Resumo dos filmes lançados no ano de {year}")

col1, col2, col3, col4 = st.columns(4)

mean = df.year['imdb_score'].dropna().mean()

if pd.isna(mean):
    mean = 0

col1.metric(label="Filmes lançados", value=df.year.shape[0])
col2.metric(label="Média do IMDb", value=f"{mean:.2f}")

def gettop(df, column):
    df = df.copy()
    df[column] = df[column].dropna().apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    return (
        df.explode(column)[column]
        .value_counts()
        .idxmax()
    )

col3.metric(label="Gênero mais comum", value=(gettop(df.year, 'genres')))
col4.metric(label="País mais comum", value=(gettop(df.year, 'production_countries')))    





attributes = ['title', 'release_year', 'imdb_score', 'imdb_votes', 'production_countries', 'genres']

st.dataframe(
    df.year[attributes].rename(columns={
    'title': 'Título',
    'release_year': 'Ano',
    'imdb_score': 'Nota IMDb',
    'imdb_votes': 'Votos',
    'production_countries': 'Países',
    'genres': 'Gêneros'
             }), hide_index=True
    )