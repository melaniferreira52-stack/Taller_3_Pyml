import requests
from django.conf import settings
from django.shortcuts import render


def tasador(request):
    contexto = {}

    if request.method == 'POST':
        area_raw = request.POST.get('area_m2', '').strip()
        contexto['area_ingresada'] = area_raw

        try:
            area_m2 = float(area_raw)
            if area_m2 <= 0:
                raise ValueError

            respuesta = requests.post(
                f'{settings.API_URL}/predict',
                json={'area_m2': area_m2},
                timeout=5,
            )
            respuesta.raise_for_status()
            data = respuesta.json()

            contexto['exito'] = True
            contexto['area_m2'] = data.get('area_m2')
            contexto['precio_estimado'] = data.get('predicted_price')

        except ValueError:
            contexto['error'] = 'Ingresa un número válido (ej: 85.5).'
        except requests.exceptions.ConnectionError as e:
            contexto["error"] = f"No fue posible conectar: {e}"
        except requests.exceptions.RequestException as e:
            contexto['error'] = f'Ocurrió un error al calcular el precio: {e}'

    return render(request, 'app_predicc/index.html', contexto)