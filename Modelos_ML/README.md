# 🏠 Tasador de Viviendas

Proyecto de Machine Learning con **FastAPI** (backend, regresión lineal) y **Django** (frontend), desplegado en **Railway** usando Docker.

Dado un área en m², la API predice el precio estimado de la vivienda; el frontend en Django ofrece un formulario simple para consultarlo.

---

## 📁 Estructura del proyecto

```
taller3_py/
└── Modelos_ML/
    └── RegresionLineal/
        ├── back/                       # API en FastAPI
        │   ├── Dockerfile
        │   ├── main.py                 # Endpoint POST /predict
        │   ├── train.py                # Entrena y guarda el modelo
        │   ├── requirements.txt
        │   └── models/
        │       └── linear_model.joblib
        │
        └── front/                      # Interfaz en Django
            ├── Dockerfile
            ├── manage.py
            ├── requirements.txt
            ├── .gitignore
            ├── config/                 # settings, urls, wsgi, asgi
            └── app_predicc/            # vista, template, CSS
```

---

## ⚙️ Backend — FastAPI

### Qué hace

- `POST /predict` recibe `{"area_m2": 85.5}` y devuelve `{"area_m2": 85.5, "predicted_price": 194505.83}`.
- El modelo de regresión lineal se entrena con `train.py` y se guarda en `models/linear_model.joblib`.
- Documentación automática disponible en `/docs` (Swagger) y `/redoc` (ReDoc).

### Correr en local

```bash
cd back
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
python train.py                    # genera el modelo .joblib
uvicorn main:app --reload --port 8000
```

Prueba en: `http://127.0.0.1:8000/docs`

---

## 🖥️ Frontend — Django

### Qué hace

- Muestra un formulario ("Tasador de Viviendas") donde se ingresa el área en m².
- Al enviarlo, hace una petición `POST` al backend (`API_URL + /predict`) usando la librería `requests`, **desde el servidor** (no desde el navegador), por lo que no hace falta configurar CORS en el backend.
- Muestra el precio estimado o un mensaje de error si no logra conectarse.

### Variable de entorno clave

```python
# config/settings.py
API_URL = os.environ.get('API_URL', 'http://127.0.0.1:8000')
```

⚠️ **`API_URL` es solo la base del dominio, sin `/predict` al final** — el propio código de `views.py` le agrega esa ruta al hacer la petición. Ponerle `/predict` de más en la variable duplica la ruta y rompe la conexión.

### Correr en local

```bash
cd front
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8080
```

Con el backend corriendo en el puerto 8000 en otra terminal, abre `http://127.0.0.1:8080/`.

---

## 🐳 Desplegar todo con Docker (en tu propia máquina)

Desde `Modelos_ML/RegresionLineal/` (donde está el `docker-compose.yml`):

```bash
docker compose up --build
```

| Servicio | URL local |
|---|---|
| Frontend | http://localhost:8080/ |
| Backend (health check) | http://localhost:8000/ |
| Swagger | http://localhost:8000/docs |

Comandos útiles:
```bash
docker compose logs -f          # ver logs en vivo
docker compose down             # parar los contenedores
docker compose build --no-cache # reconstruir sin caché
```

---

## 🚂 Desplegar en Railway (producción)

Cada servicio (`back` y `front`) se despliega como un **servicio independiente** dentro del mismo proyecto de Railway, ambos apuntando al mismo repositorio de GitHub pero con distinto **Root Directory**.

### 1. Backend

1. Railway → **New → GitHub Repo** → selecciona el repo.
2. En **Settings → Source → Root Directory**, escribe:
   ```
   Modelos_ML/RegresionLineal/back
   ```
3. Railway detecta el `Dockerfile` solo y construye la imagen.
4. **Settings → Networking → Generate Domain** para obtener la URL pública.
5. Prueba `https://<tu-dominio>.up.railway.app/docs` — debe cargar el Swagger.

### 2. Frontend

1. Railway → **New → GitHub Repo** (mismo repo) → Root Directory:
   ```
   Modelos_ML/RegresionLineal/front
   ```
2. **Variables** → agrega:
   ```
   API_URL = https://<dominio-del-backend>.up.railway.app
   ```
   (sin `/predict`, sin `/` sobrante al final).
3. **Settings → Networking → Generate Domain**. En "Enter the port your app is listening on", pon el mismo puerto que tu `Dockerfile`/`CMD` usa internamente (revisa el Deploy Log: aparece como `Listening at: http://0.0.0.0:XXXX`).
4. Prueba la URL pública del frontend con un cálculo real.

### Ajustes que necesita Django para funcionar en Railway

En `config/settings.py`:

```python
ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://<dominio-del-frontend>.up.railway.app']
```

- `ALLOWED_HOSTS` — sin esto, Django rechaza cualquier petición que no venga de `localhost`.
- `CSRF_TRUSTED_ORIGINS` — sin esto, el formulario tira **403 Forbidden (CSRF verification failed)** al enviarse. **El valor debe incluir el esquema `https://`** — Django 4+ lo exige, no basta con poner solo el dominio.

### Servir el CSS en producción (Whitenoise)

El servidor de desarrollo (`runserver`) sirve el CSS automáticamente; **gunicorn (producción) no lo hace por diseño**. Para que el CSS cargue en Railway:

**`requirements.txt`:**
```
Django==5.0.6
requests==2.32.3
gunicorn==22.0.0
whitenoise==6.7.0
```

**`config/settings.py`** — agregar al `MIDDLEWARE`, justo después de `SecurityMiddleware`:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
```

Y al final del archivo:
```python
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**`Dockerfile`** — correr `collectstatic` antes de arrancar gunicorn:
```dockerfile
CMD python manage.py collectstatic --noinput && python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000}
```

---

## 🐛 Errores comunes y cómo se resolvieron

| Error | Causa | Solución |
|---|---|---|
| `Railpack could not determine how to build the app` | Faltaban `Dockerfile` y/o `requirements.txt` en la carpeta, o no se subieron a GitHub | Crear ambos archivos y confirmar con `git status` que sí se subieron |
| `Application failed to respond` (502) | El puerto configurado en "Generate Domain" no coincide con el puerto real donde escucha gunicorn | Revisar el Deploy Log (`Listening at: http://0.0.0.0:XXXX`) y usar ese mismo número |
| `CSRF verification failed. Origin checking failed` | Falta `CSRF_TRUSTED_ORIGINS` en `settings.py` | Agregarlo con el dominio del frontend, incluyendo `https://` |
| `CSRF_TRUSTED_ORIGINS setting must start with a scheme` | Se puso el dominio sin `https://` | Agregar el esquema completo: `https://dominio.up.railway.app` |
| CSS no carga en producción (se ve sin estilos) | Gunicorn no sirve archivos estáticos por defecto | Instalar y configurar `whitenoise` + `collectstatic` |
| `HTTPConnectionPool(host='127.0.0.1', port=8000)... Connection refused` | La variable `API_URL` no estaba definida (o mal escrita) en Railway, y el código usaba el valor local por defecto | Verificar el nombre exacto de la variable (`API_URL`) y su valor en Railway |
| Ruta duplicada tipo `/predic/predict` | Se puso la URL completa del endpoint (copiada de Swagger, incluyendo `/predict`) en la variable `API_URL` | `API_URL` debe ser solo la base del dominio — el código ya agrega `/predict` |
| `ImportError: Couldn't import Django` en local | El entorno virtual `.venv` no estaba activado en esa terminal | Activar con `.venv\Scripts\Activate.ps1` en cada terminal nueva antes de correr comandos |

---

## ✅ Checklist final

- [x] Backend con `/predict`, `/docs` y `/redoc` funcionando en Railway
- [x] Frontend en Django desplegado en Railway, conectado al backend vía `API_URL`
- [x] CSS cargando correctamente en producción (Whitenoise)
- [x] Sin errores de CSRF ni de `ALLOWED_HOSTS`
- [x] Repositorio en GitHub con `back/` y `front/` como carpetas hermanas