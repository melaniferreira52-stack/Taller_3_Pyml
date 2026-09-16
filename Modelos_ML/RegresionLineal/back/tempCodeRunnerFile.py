y_pred = model.predict(x)

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