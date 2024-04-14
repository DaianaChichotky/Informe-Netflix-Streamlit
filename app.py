# Importamos librerias necesarias para el Proyecto:

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import streamlit as st
from sklearn.preprocessing import LabelEncoder

# Configuramos la Página

# 1) layout="centered" or "wide"

st.set_page_config(page_title='Informe sobre Netflix', layout='wide', page_icon='👋')
logo = 'https://assets-global.website-files.com/5ee732bebd9839b494ff27cd/5ee732bebd98393d75ff281d_580b57fcd9996e24bc43c529.png'


# 2) Columnas

col1, col2, col3 = st.columns(3)
with col1 :
    st.write("Estudio realizado por Daiana Chichotky")
    st.write('14/04/2024')
with col2 :
    st.image(logo, width=400)
    st.title('Informe sobre Netflix')
with col3 :
    st.write('')


# 3) Sidebar

st.sidebar.image(logo, width=200)
st.sidebar.title('Menú')
st.sidebar.subheader('Filtros')
st.sidebar.write('-------')

# 4) Cosas que vamos a usar en toda la App

df = pd.read_csv(r'C:\Users\Dai\Desktop\Bootcamp_Upgrade_Hub\GitHub\Informe-Netflix\data\netflixprocesado.csv')
if "Unnamed: 0" in df:
    df = df.drop(columns=["Unnamed: 0"])  # Eliminamos la columna Unnamed: 0
else:
    pass

#st.dataframe(df.head())
st.write('Datos obtenidos luego del análisis de nuestra base de datos de Netflix:')


# 5) Sidebar

# 5.1) Sidebar Filtro 1:

# CREAR UNA VAR CON EL FILTRO

filtro_pais = st.sidebar.selectbox('País', df['País'].unique())
if filtro_pais:
    df1 = df.loc[df['País'] == filtro_pais]


# 5.2) Sidebar Filtro 2:

filtro_genero = st.sidebar.selectbox('Tipo', df['Tipo'].unique())
if filtro_genero:
    df1 = df.loc[df['Tipo'] == filtro_genero]


# 6) Union de filtros (Para usar en la Tab 1)

if filtro_pais and filtro_genero:
    df2 = df.loc[(df['País'] == filtro_pais) & (df['Tipo'] == filtro_genero)]

# 7) Tabs

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    [
        "Base de datos Netflix filtrada",
        "Paises en los que se han visto más peliculas",
        "Peliculas que duran más de 1.30h",
        "Actor que más peliculas tiene en Netflix",
        "Top 3 de series de comedia más vistas",
        "Puntuacion mas común",
        "Correlación entre las variables",
        "Peliculas con mejores puntuaciones"
    ]
)

# --------------------TAB 1----------------------------#
#Base de datos Netflix filtrada

with tab1:
    st.dataframe(df2)

# --------------------TAB 2----------------------------#
#Paises en los que se han visto más peliculas

with tab2:
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write('¿En que país se vieron más películas?')
            df_pais = df['País'].value_counts().reset_index()
            st.dataframe(df_pais.head(3))
        with col2:
            fig = px.bar(df_pais.head(3), x='count', y='País', title='Top 3 de países con más películas')
            st.plotly_chart(fig)

# --------------------TAB 3----------------------------#
#Peliculas que duran más de 1.30h

with tab3:
    #elimininamos los nulos
    df = df.dropna()  
    st.write('Películas que duran más de 1.30h')
    df_movies = df[df['Tipo'] == 'Movie']
    df_movies['Duración'] = df_movies['Duración'].str.replace(' min', '').astype(int)
    df_duracion = df_movies[df_movies['Duración'] > 90]
    st.dataframe(df_duracion)
    st.write('Número de películas que duran más de 1.30h:', df_duracion.shape[0])
    fig = px.histogram(df_duracion, x='Duración', title='Duración de las películas')
    st.plotly_chart(fig)

# --------------------TAB 4----------------------------#
#Actor que más peliculas tiene en Netflix

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        st.write('¿Cuál es el actor que más películas tiene en Netflix?')
        df_actor = df['cast'].str.split(', ', expand=True).stack().value_counts().reset_index()
        df_actor.columns = ['cast', 'Películas']
        st.dataframe(df_actor.head(1))
    with col2:
        fig = px.bar(df_actor.head(10), x='cast', y='Películas', title='Top 10 de actores con más películas')
        st.plotly_chart(fig)

# --------------------TAB 5----------------------------#
#Top 3 de series de comedia más vistas

with tab5:
    st.write('¿Cuál es el top 3 de series de comedia más vistas?')
    #Comedies se encuentra dentro de la columna Listada_en junto con otros géneros
    df_comedies = df[df['Listada_en'].str.contains('Comedies')]
    #filtramos ahora por tipo Tv Show
    df_comedies = df_comedies[df_comedies['Tipo'] == 'TV Show']
    st.dataframe(df_comedies)
    

# --------------------TAB 6----------------------------#
#Puntuacion mas común

with tab6:
    col1, col2 = st.columns(2)
    with col1:
        st.write('¿Cuál es la puntuación más común?')
        #value counts de la columna Puntuación
        df_puntuacion = df['Puntuación'].value_counts().reset_index()
        df_puntuacion.columns = ['Puntuación', 'Número de películas']
        st.dataframe(df_puntuacion)
    with col2:
        fig = px.bar(df_puntuacion, x='Puntuación', y='Número de películas', title='Puntuación de las películas')
        st.plotly_chart(fig)

# --------------------TAB 7----------------------------#
#Correlación entre las variables

with tab7:
    
    le = LabelEncoder()
    df_encoded = df.copy()
    for col in df_encoded.columns:
        if df_encoded[col].dtype == 'object':
            df_encoded[col] = le.fit_transform(df_encoded[col])
    corr = df_encoded.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# --------------------TAB 8----------------------------#
#Peliculas con mejores puntuaciones

with tab8:
    st.write('Películas con mejores puntuaciones')
    df_puntuacion = df.sort_values(by='Puntuación', ascending=False)
    st.dataframe(df_puntuacion.head(10))