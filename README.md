# Taller 3 - 🤖

¡Hola! Este es mi taller #3, aquí les cuento rapidito qué hice y dónde encontrar cada cosa 😊

## 📁 ¿Qué hay en este repo?

Dentro de `Modelos_ML` tengo tres proyectos:

### 1. 🩺 RandomForest → Diagnóstico Clínico con IA

Este proyecto usa un modelo de Random Forest (que es como armar muchos "árboles de decisión" y entre todos votan cuál es la respuesta más probable) para predecir qué enfermedad podría tener un paciente según sus síntomas y signos vitales. Puede identificar 5 posibles diagnósticos: infarto, neumonía, gripe, ansiedad o gastroenteritis. Tiene 3 pasitos:

- **`1.Crear_dataset.py`** → genera un dataset de pacientes "de mentiras" (simulados) con edad, presión, síntomas, etc., para poder entrenar el modelo con él.
- **`2.Entrenar_modelo.py`** → toma ese dataset y entrena el Random Forest, luego lo guarda ya entrenado en la carpeta `models/`.
- **`3.Predecir_enfermedad.py`** → es la app hecha en Streamlit donde uno llena un formulario con los síntomas del paciente y el modelo dice cuál enfermedad es más probable, con el porcentaje de confianza y una recomendación.

Para correrlo toca instalar lo que pide `requirements.txt` y ejecutar los 3 pasos en orden (primero crear el dataset, luego entrenar, y al final correr el `3.Predecir_enfermedad.py` con el comando `streamlit run`).

🔗 URL del Sistema de Diagnostico Clinico, desplegado en Streamlit: https://taller3pyml-mcusts94hsmso6tn5c32gs.streamlit.app/ 

---

### 2. 🏠 RegresionLineal → el Tasador de Viviendas

Aquí hice un modelo de regresión lineal que, dándole el área de una casa en m², le calcula el precio estimado. Está dividido en dos carpetitas:

- **`back/`** → es la API hecha en FastAPI, aquí es donde vive el modelo entrenado y donde se hace la predicción (recibe el área y devuelve el precio).
- **`front/`** → es la interfaz hecha en Django, o sea la páginita donde uno escribe el área en un formulario y le da clic para ver el resultado.

🔗 URL del Tasador de Viviendas, desplegado en Railway (back y front):

BACKEND - https://backend-production-fd67d.up.railway.app/

FRONTEND - https://frontend-production-60d5d.up.railway.app/

---

### 2. 📷 VisionArtificial → el Detector de Rostros

Este es el proyecto donde trabajamos con visión artificial usando OpenCV. La app detecta rostros ya sea subiendo una imagen o usando la cámara en vivo, y dibuja un recuadro verde alrededor de cada cara que encuentra, contándolas también.

🔗 URL del Detector de Rostros, desplegado en Vercel: https://py-img-main.vercel.app/ 