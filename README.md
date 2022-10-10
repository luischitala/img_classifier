# Saturdays 3ra edición despliegue de modelos

## Tabla de contenidos:
- [ Saturdays 3ra edición despliegue de modelos](#Saturdays-3ra-edición-despliegue-de-modelos)
  - [Tabla de contenidos:](#table-of-contents)
  - [Descripción](#descripción)
  - [Requisitos:](#requisitos)
  - [Dependencias relevantes:](#dependencias-relevantes)
  - [Instalación](#instalacion)
    - [Con docker](#con-docker)
    - [Sin docker](#sin-docker)
  - [Uso Básico](#uso-basico)


## Descripción
Este proyecto está conformado por una API sencilla creada con FastAPI para mostrar le despliegue de un modelo de clasificación de imágenes usando Keras.

Este clasificador está entrenado con imágenes de aviones y autos, por lo que se recomienda solo ingresar imágenes de estos tipos. Una vez realizada la clasificación, registra en una base de datos la categorpia predicha y los datos de la imagen. 

Se puede acceder a dos jupyter notebooks, las cuales están localizadas en la carpeta classifiers/.

## Requisitos:
- Docker and Docker Compose (Opcional)
- Python >= 3.6

## Dependencias Relevantes:
- FastAPI == 0.75.2
- Uvicorn == 0.17.6
- keras
- tensorflow

## Instalación
1. Clonar o descargar el repositorio:
    ```
    git clone https://github.com/luischitala/img_classifier
	cd img_classifier
    ```

### Con docker
1. Ejecutar con Docker Compose.
    ```bash
    docker-compose -f .\api\deployment\docker-compose.yml up -d
    ```

### Sin docker
1. Crear un entorno virtual
    ```bash
    python -m venv venv
    ```
2. Activar entorno virtual
    ```bash
	.\venv\Scripts\activate
	o
	source ./venv/bin/activate
    ```
3. Istalar las dependencias
    ```bash
	pip install -r ./api/deployment/api/requirements.txt
    ```
4. Correr la aplicación
    ```bash
    uvicorn main:app --reload
    ```
## Uso Básico
Si se ejecutó con docker la dirección es: [http:127.0.0.1:8080/docs](http://localhost:8080/docs) para entrar a la documentación. 

	Por el contrario sin docker la dirección es: [http:127.0.0.1:8000/docs](http://localhost:8000/docs) para entrar a la documentación. 
	
	El endpoint para la claficación de imágenes es: /upload

	## Referencias y reconocimiento a:  [geeksforgeeks](https://www.geeksforgeeks.org/python-image-classification-using-keras)

	https://towardsdatascience.com/implementing-fastapi-in-10-minutes-d161cdd7c075
	https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
