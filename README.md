# Proyecto de Recomendación de Películas
## Descripción
Este proyecto consiste en un sistema de recomendación de películas basado en la similaridad de los títulos utilizando técnicas de procesamiento de lenguaje natural y cálculo de similaridad del coseno. El sistema está implementado utilizando FastAPI para la creación de la API y se apoya en bibliotecas como Pandas, Scikit-Learn y Uvicorn.

## Requisitos
- Python 3.8 o superior

- FastAPI

- Uvicorn

- Pandas

- Scikit-Learn

Puedes instalar las dependencias necesarias utilizando el siguiente comando:

```bash
pip install fastapi uvicorn pandas scikit-learn
```


## Estructura del Proyecto

```bash
proyecto_recomendacion/
│
├── datasets/
│   └── dataset_unificado.csv
│   └── dataset_filtrado_10000.csv
│
├── main.py
│
├── requirements.txt
│
└── README.md
```

- `datasets/dataset_unificado.csv`: Archivo CSV con los datos de las películas.

- `main.py`: Archivo principal con el código de la API.

- `requirements.txt`: Lista de dependencias necesarias para el proyecto.

- `README.md`: Archivo con la documentación del proyecto.

## Configuración y Ejecución

1. Clona el repositorio:

```bash
git clone https://github.com/KevGuarda/Henry_PI1_recomendacion.git
cd proyecto_recomendacion
```

2. Asegúrate de tener un entorno virtual y actívalo:

```bash
python -m venv env
source env/bin/activate
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecuta la aplicación:

```bash
uvicorn main:app --reload
```

La aplicación estará disponible en `http://127.0.0.1:8000`.

## Endpoints

`/cantidad_filmaciones_mes/`

Devuelve la cantidad de filmaciones realizadas en un mes específico.

Parámetro: `mes` (str)

`/cantidad_filmaciones_dia/`

Devuelve la cantidad de filmaciones realizadas en un día específico.

- Parámetro: `dia` (str)

`/score_titulo/`

Devuelve el score de popularidad de una película específica.

- Parámetro: `titulo_de_la_filmacion` (str)

`/votos_titulo/`

Devuelve el número de votos de una película específica.

- Parámetro: `titulo_de_la_filmacion` (str)

`/get_actor/`

Devuelve información sobre un actor específico.

- Parámetro: `nombre_actor` (str)

`/get_director/`

Devuelve información sobre un director específico.

- Parámetro: `nombre_director` (str)

`/recomendacion/`

Devuelve una lista de películas recomendadas basadas en la similaridad del título.

- Parámetro: `titulo` (str)

## Ejemplo de Uso

Puedes probar los endpoints utilizando herramientas como curl o Postman. A continuación, se muestra un ejemplo utilizando curl para obtener recomendaciones de películas similares a "Batman":

```bash
curl -X GET "http://127.0.0.1:8000/recomendacion/?titulo=Batman"
```

## Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir issues o pull requests.

## Video Explicativo

En el siguiente enlace podrán ver un video explicativo del proyecto: https://drive.google.com/file/d/1qUKAcVeVgoy5P0c5MwM9-P1q8bZJm8p_/view?usp=sharing.
