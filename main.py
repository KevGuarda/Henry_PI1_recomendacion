from fastapi import FastAPI, Query
from typing import Dict, List, Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Crear la aplicación FastAPI
app = FastAPI()

# Cargar la base de datos 'dataset_unificado'
df_merged = pd.read_csv("datasets/dataset_unificado.csv", sep=",")

# Asegúrate de que la columna 'release_date' está en formato de fecha
df_merged['release_date'] = pd.to_datetime(df_merged['release_date'])

# Añadir una columna para el año de lanzamiento
df_merged['release_year'] = df_merged['release_date'].dt.year

# Diccionario para convertir meses en español a números
meses = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}

# Diccionario para convertir días de la semana en español a números (0=lunes, 6=domingo)
dias_semana = {
    "lunes": 0,
    "martes": 1,
    "miércoles": 2,
    "jueves": 3,
    "viernes": 4,
    "sábado": 5,
    "domingo": 6
}

@app.get("/cantidad_filmaciones_mes/")
async def cantidad_filmaciones_mes(mes: str = Query(..., description="Ingrese aquí el mes")) -> Dict[str, Any]:
    mes = mes.lower()
    if mes not in meses:
        return {"error": "Mes no válido"}

    mes_numero = meses[mes]
    cantidad = df_merged[df_merged['release_date'].dt.month == mes_numero].shape[0]

    return {"message": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes.capitalize()}"}

@app.get("/cantidad_filmaciones_dia/")
async def cantidad_filmaciones_dia(dia: str = Query(..., description="Ingrese aquí el día")) -> Dict[str, Any]:
    dia = dia.lower()
    if dia not in dias_semana:
        return {"error": "Día no válido"}

    dia_numero = dias_semana[dia]
    cantidad = df_merged[df_merged['release_date'].dt.dayofweek == dia_numero].shape[0]

    return {"message": f"{cantidad} cantidad de películas fueron estrenadas en los días {dia.capitalize()}"}

@app.get("/score_titulo/")
async def score_titulo(titulo_de_la_filmacion: str = Query(..., description="Ingrese aquí el título de la filmación")) -> Dict[str, Any]:
    pelicula = df_merged[df_merged['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if pelicula.empty:
        return {"error": "Película no encontrada"}

    titulo = pelicula.iloc[0]['title']
    año_estreno = pelicula.iloc[0]['release_year']
    popularidad = pelicula.iloc[0]['popularity']

    return {"message": f"La película '{titulo}' fue estrenada en el año {año_estreno} con un score/popularidad de {popularidad}"}

@app.get("/votos_titulo/")
async def votos_titulo(titulo_de_la_filmacion: str = Query(..., description="Ingrese aquí el título de la filmación")) -> Dict[str, Any]:
    pelicula = df_merged[df_merged['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if pelicula.empty:
        return {"error": "Película no encontrada"}

    votos = pelicula.iloc[0]['vote_count']
    if votos < 2000:
        return {"message": "La película no cuenta con al menos 2000 valoraciones, no se devuelve ningún valor"}

    titulo = pelicula.iloc[0]['title']
    año_estreno = pelicula.iloc[0]['release_year']
    promedio_votos = pelicula.iloc[0]['vote_average']

    return {"message": f"La película '{titulo}' fue estrenada en el año {año_estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio_votos}"}

@app.get("/get_actor/")
async def get_actor(nombre_actor: str = Query(..., description="Ingrese aquí el nombre del actor")) -> Dict[str, Any]:
    peliculas_actor = df_merged[df_merged['cast_names'].str.contains(nombre_actor, case=False, na=False)]
    if peliculas_actor.empty:
        return {"error": "Actor no encontrado"}

    total_retorno = peliculas_actor['return'].sum()
    cantidad_peliculas = peliculas_actor.shape[0]
    promedio_retorno = total_retorno / cantidad_peliculas

    return {
        "message": f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_retorno} con un promedio de {promedio_retorno:.2f} por filmación"
    }

@app.get("/get_director/")
async def get_director(nombre_director: str = Query(..., description="Ingrese aquí el nombre del director")) -> Dict[str, Any]:
    peliculas_director = df_merged[df_merged['directing_names'].str.contains(nombre_director, case=False, na=False)]
    if peliculas_director.empty:
        return {"error": "Director no encontrado"}

    total_retorno = peliculas_director['return'].sum()
    detalles_peliculas = peliculas_director[['title', 'release_date', 'return', 'budget', 'revenue']].to_dict(orient='records')

    for pelicula in detalles_peliculas:
        pelicula['release_date'] = pelicula['release_date'].strftime("%Y-%m-%d")

    return {
        "message": f"El director {nombre_director} ha conseguido un retorno total de {total_retorno}",
        "detalles_peliculas": detalles_peliculas
    }

# Función de Recomendación

# Cargar la base de datos 'dataset_unificado'
df_filtered = pd.read_csv("datasets/dataset_filtrado_10000.csv", sep=",")

# Preprocesamiento de Datos - Utilizando 'title' para la recomendación
df_filtered['title'] = df_filtered['title'].fillna('')

# Vectorización de Textos - Usar TfidfVectorizer para transformar los títulos en vectores
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df_filtered['title'])

# Cálculo de Similaridad - Utilizar la similaridad del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Crear una serie con los títulos de las películas como índice
indices = pd.Series(df_filtered.index, index=df_filtered['title']).drop_duplicates()

def get_recommendations(title, cosine_sim, df_filtered):
    # Normalizar el título
    title = title.strip().lower()  # Eliminar espacios y convertir a minúsculas
    
    # Obtener el índice de la película que coincide con el título
    matching_movies = df_filtered[df_filtered['title'].str.lower().str.contains(title)]
    
    if matching_movies.empty:
        raise ValueError(f"No se encontró ninguna película con el título: '{title}'")

    idx = matching_movies.index[0]
    
    # Obtener las puntuaciones de similaridad para esa película
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas basadas en las puntuaciones de similaridad
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener las puntuaciones de las 5 películas más similares
    sim_scores = sim_scores[1:6]  # Cambiado a 5

    # Obtener los índices de las películas
    movie_indices = [i[0] for i in sim_scores]

    # Devolver los títulos de las películas recomendadas
    return df_filtered['title'].iloc[movie_indices].tolist()

# Crear el endpoint de recomendación
@app.get("/recomendacion/")
async def recomendacion(titulo: str = Query(..., description="Ingrese aquí el título de la película")) -> List[str]:
    return get_recommendations(titulo, cosine_sim, df_filtered)
