import joblib 
from pathlib import Path
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

#predecir precios de viviendas según la superficie en M2

#datos de entrenamiento (x) y etiquetas (y)
x = np.array([[40], [50], [60], [85], [100], [150]])
y = np.array([100000, 120000, 150000, 200000, 250000, 300000])

#entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(x, y)

#predicciones de prueba
# y_pred = model.predict(x)

# #imprimir la informacion del modelo entrenado
# print("Coeficiente de regresión:", model.coef_[0])
# print("Término independiente:", model.intercept_)

# #graficar datos reales
# plt.scatter(x, y, color='red', label='Datos de entrenamiento')

# #graficar los datos de entrenamiento y la linea de regresion
# plt.plot(x, y_pred, color='blue', label='Línea de regresión')

# plt.xlabel('Superficie (m2)')
# plt.ylabel('Precio (COP)')
# plt.title('Regresión Lineal: Precio de Viviendas según Superficie')
# plt.legend()
# plt.grid(True)

# #Imprimir la grafica
# plt.show()

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"

#guardar el modelo entrenando en un archivo
joblib.dump(model, MODEL_PATH)