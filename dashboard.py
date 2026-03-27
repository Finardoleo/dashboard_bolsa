import streamlit as st
import pandas as pd
import plotly.express as px 

st.set_page_config(page_title="Dashboard de Secas 2015", page_icon="icon.jpg", layout="wide")

df = pd.read_csv('Secas.csv', sep=',', decimal='.')

estado = st.sidebar.selectbox('Selecione o estado', df['NM_ESTADO'].unique())


df.filtered = df[df['NM_ESTADO'] == estado] 

st.header('Análise de Secas - 2015')


total_municipios = df.filtered.shape[0]
afetados = df.filtered[df.filtered['SECAS2015'] == 1].shape[0]
percentual = (afetados / total_municipios * 100) if total_municipios > 0 else 0
area_total = df.filtered['SHAPE_Area'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric('Municípios', total_municipios)
col2.metric('Com seca', afetados)
col3.metric('Afetados %', f"{percentual:.1f}%")
col4.metric('Área total', f"{area_total:.2f}")





col_graf1, col_graf2 = st.columns(2)


fig1 = px.histogram(
    df.filtered,
    x='SHAPE_Area',
    color='SECAS2015',
    title='Distribuição de Área (Seca vs Não seca)',
    labels={'SHAPE_Area': 'Área'}
)
col_graf1.plotly_chart(fig1, use_container_width=True)




fig2 = px.scatter(
    df.filtered,
    x='SHAPE_Area',
    y='SHAPE_Length',
    color='SECAS2015',
    title='Área vs Perímetro',
    labels={'SHAPE_Area': 'Área', 'SHAPE_Length': 'Perímetro' } 
)
col_graf2.plotly_chart(fig2, use_container_width=True)




st.subheader('Top 10 maiores municípios com seca')

top10 = (
    df.filtered[df.filtered['SECAS2015'] == 1]
    .sort_values('SHAPE_Area', ascending=False)
    .head(10)
)

st.dataframe(top10)


st.subheader('Dados filtrados')
st.dataframe(df.filtered)
