import streamlit as st
import pandas as pd
import plotly.express as px 
import ast

#Configurações da página 

st.set_page_config(page_title="Cinescópio", page_icon="icon.jpg", layout="wide")

#Ler o dataset

df = pd.read_csv('movies.csv', sep=',', decimal='.')


#Adicionar sidebar para selecionar ano e filtrar os dados pelo ano

year = st.sidebar.selectbox('Selecione o ano', sorted(df.release_year.unique(), reverse=True))
df.year = df[df['release_year'] == year] 




#Título e descrição do dashboard com explicação e uma divisão visual para separar a seção dos resumos

st.header(f"Resumo dos filmes lançados no ano de {year}")

st.markdown(f"Este dashboard apresenta um resumo dos filmes lançados no ano de {year}, com base nos dados disponíveis. Aqui estão disponíveis as informações sobre a quantidade de produções, a média das notas do IMDb, além de uma tabela detalhada com as informações de cada filme lançado no ano de {year} armazenados na database.")

st.divider(width='stretch')



#Separação das páginas em diferentes colunas 

col1, col2, col3, col4 = st.columns(4)
col5, col6, col7, col8 = st.columns(4) 
col9, col10 = st.columns(2) 
col11, col12 = st.columns(2)      


#Declaração de variáveis e filtros 

mean = df.year['imdb_score'].dropna().mean()

df.countries = (df.year['production_countries'].apply(ast.literal_eval)).explode()

df.genre = (df.year['genres'].apply(ast.literal_eval)).explode()



df.score = df.year.copy()
df.score['genres'] = (df.score['genres']).apply(ast.literal_eval)
df.score = df.score.explode('genres')

df.score = (
    df.score.groupby('genres')['imdb_score']
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

topgenres = df.genre.value_counts().head(10).reset_index()
topgenres.columns = ['genre', 'count']
topgenres = topgenres.sort_values(by='count')  


topcountries = df.countries.value_counts().head(10).reset_index()
topcountries.columns = ['country', 'count']
topcountries = topcountries.sort_values(by='count')

if pd.isna(mean):
    mean = 0



#Exibição dos dados simples 


col1.metric(label='Produções lançados', value=df.year.shape[0]) 
col2.metric(label='Filmes', value=df.year[df.year['type'] == 'MOVIE'].shape[0])
col3.metric(label='Séries', value=df.year[df.year['type'] == 'SHOW'].shape[0])
col4.metric(label='Média do IMDb', value=f"{mean:.2f}") 


col5.metric(label='Votos totais', value=int(df.year['imdb_votes'].sum()))
col6.metric(label='Duração média', value=f"{df.year['runtime'].dropna().mean():.2f} min")
col7.metric(label='Países únicos', value=df.countries.nunique())
col8.metric(label='Gêneros únicos', value=df.genre.nunique())



#Exibição do gráfico de barra com os 10 gêneros mais populares 

fig_generos = px.bar(
    topgenres,
    x='count',
    y='genre',
    orientation='h',
    title='Os 10 gêneros mais populares',

    labels={
        'count': 'Quantidade de Filmes',
        'genre': 'Gênero'
    }
)

col9.plotly_chart(fig_generos, use_container_width=True)




#Exibição do gráfico de barra com os 10 maiores países produtores de filmes 

fig_paises = px.bar(
    topcountries,
    x='count',
    y='country',
    orientation='h',
    title='Os 10 maiores países produtores',

    labels={
        'count': 'Quantidade de Filmes',
        'country': 'País'
    }
)

col10.plotly_chart(fig_paises, use_container_width=True)



#Exibição do histograma com as distribuições das nodas IMDb

fig_hist = px.histogram(
    df.year,
    x='imdb_score',
    nbins=20,
    title='Distribuição das Notas IMDb',
    labels={
        'imdb_score': 'Nota IMDb'
        }
)

fig_hist.update_layout(
    yaxis_title='Quantidade de Filmes',
)

col11.plotly_chart(fig_hist, use_container_width=True)




#Exibição do boxplot com as distribuições das nodas IMDb

fig_box = px.box(
    df.year,
    y='imdb_score',
    title='Distribuição (Boxplot) das Notas IMDb',
    labels={'imdb_score': 'Nota IMDb'}
)

col12.plotly_chart(fig_box, use_container_width=True)





#Exibição do gráfico de barra com os 10 gêneros com melhor avaliação média no IMDb 

st.divider(width='stretch')

fig_genre_score = px.bar(
    df.score,
    x='imdb_score',
    y='genres',
    orientation='h',
    title='Gêneros com Melhor Avaliação Média',
    labels={
        'imdb_score': 'Nota Média',
        'genres': 'Gênero'
    }
)

st.plotly_chart(fig_genre_score, use_container_width=True)







#Separação visual para a seção da tabela bruta dos filmes lançados no ano selecionado 

st.divider(width='stretch')

st.header(f"Filmes lançados no ano de {year}")

st.divider(width='stretch')


#Tabela bruta dos filmes daquele ano 

attributes = ['title', 'runtime', 'imdb_score', 'imdb_votes', 'production_countries', 'genres']

st.dataframe(
    df.year[attributes].rename(columns={
    'title': 'Título',
    'runtime': 'Duração (min)', 
    'imdb_score': 'Nota IMDb',
    'imdb_votes': 'Votos',
    'production_countries': 'País de Produção',
    'genres': 'Gêneros'
             }), hide_index=True
    )