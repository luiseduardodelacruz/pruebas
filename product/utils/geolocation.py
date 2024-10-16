import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests
from django.http import JsonResponse
from urllib.parse import quote
from product.models import Alcaldia, Prediccion, Sucursales
from django.db.models import Sum, F

def get_coordinates_from_address(address):
    try:
        # Usar la API de OpenStreetMap para obtener las coordenadas
        headers = {
            'User-Agent': 'mapa_De_Sucursales/1.0 (luis2020227@gmail.com)'  # Cambia estos datos según tu aplicación
        }
        # Codificar la dirección para la URL
        encoded_address = quote(address)
        response = requests.get(f"https://nominatim.openstreetmap.org/search?q={encoded_address}&format=json", headers=headers)
        response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
        data = response.json()

        if data:
            # Obtener la primera coincidencia
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            print(f"No se encontraron coordenadas para la dirección: {address}")
            return None, None
    except requests.RequestException as e:
        print(f"Error al obtener coordenadas para la dirección {address}: {e}")
        return None, None
    
def get_markers(request):
    # Obtener solo las predicciones que tienen id_branch con latitud y longitud asociadas
    predictions = Prediccion.objects.exclude(
        id_branch__isnull=True  # Asegúrate de que hay un id_branch asociado
    ).select_related('id_branch')

    # Inicializar la lista de marcadores
    markers = []

    for pred in predictions:
        # Asegúrate de que id_branch tiene latitud y longitud
        if pred.id_branch.latitud is not None and pred.id_branch.longitud is not None:
            # Obtener los valores específicos de cada predicción
            capistrano_count = pred.cantidad_capistrano or 0
            lala_count = pred.cantidad_lala or 0
            san_rafael_count = pred.cantidad_san_rafael or 0
            fud_count = pred.cantidad_fud or 0
            villita_count = pred.cantidad_villita or 0
            zwan_count = pred.cantidad_zwan or 0
            bafar_count = pred.cantidad_bafar or 0
            chimex_count = pred.cantidad_chimex or 0
            kir_count = pred.cantidad_kir or 0
            sabori_count = pred.cantidad_sabori or 0

            # Sumar los contadores de la competencia
            competition_count = (
                lala_count + 
                san_rafael_count + 
                fud_count + 
                villita_count + 
                zwan_count + 
                bafar_count + 
                chimex_count + 
                kir_count + 
                sabori_count
            )

            # Generar la gráfica circular para cada predicción
            img_str_pie = generate_pie_chart(capistrano_count, competition_count)

            # Agregar los detalles de la predicción junto con el gráfico
            markers.append({
                'direccion': pred.id_branch.direccion,  # Acceso correcto al atributo
                'latitud': pred.id_branch.latitud,
                'longitud': pred.id_branch.longitud,
                'img_str_pie': img_str_pie
            })

    # Devolver la lista de marcadores como una respuesta JSON
    return JsonResponse(markers, safe=False)


def generate_pie_chart(capistrano_count, competition_count):
    # Datos para la gráfica
    labels = ['Capistrano', 'Competencia']
    sizes = [capistrano_count, competition_count]
    colors = ['#009975', '#FF5733']

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear la gráfica circular
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Asegurar que el gráfico sea un círculo
    ax.axis('equal')

    # Título de la gráfica
    ax.set_title('Distribución de Capistrano vs Competencia')

    # Ajustar el diseño para evitar superposiciones
    plt.tight_layout()

    # Cambiar el tamaño y color de los porcentajes
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(24)

    # Convertir la gráfica a imagen base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str_pie = base64.b64encode(buffer.getvalue()).decode()
    plt.close()  # Cerrar la gráfica para liberar memoria

    return img_str_pie


def get_markers_alcaldia(request):
    # Obtener todas las alcaldías
    alcaldias = Alcaldia.objects.all()

    # Inicializar la lista de marcadores
    markers = []

    for alcaldia in alcaldias:
        # Filtrar predicciones para la alcaldía actual usando el ID de la alcaldía
        predictions = Prediccion.objects.filter(id_alcaldia=alcaldia.id_alcaldia)

        # Sumar los valores de cantidad_capistrano para las predicciones de la alcaldía actual
        capistrano_total = predictions.aggregate(total=Sum('cantidad_capistrano'))['total'] or 0

        # Sumar los valores de los otros campos de competencia para las predicciones de la alcaldía actual
        competencia_total = predictions.aggregate(
            total=Sum(
                F('cantidad_lala') + 
                F('cantidad_san_rafael') + 
                F('cantidad_fud') + 
                F('cantidad_villita') + 
                F('cantidad_zwan') +
                F('cantidad_bafar') +
                F('cantidad_chimex') +
                F('cantidad_kir') +
                F('cantidad_sabori')
            )
        )['total'] or 0

        # Generar la gráfica circular para la alcaldía actual
        img_str_pie_alcaldia = generate_pie_chart_alcaldia(capistrano_total, competencia_total)

        # Añadir los datos del marcador
        markers.append({
            'alcaldia': alcaldia.nombre_alcaldia,
            'latitud': alcaldia.latitudes,
            'longitud': alcaldia.longitudes,
            'img_str_pie_alcaldia': img_str_pie_alcaldia
        })

    # Devolver la lista de marcadores como una respuesta JSON
    return JsonResponse(markers, safe=False)



def generate_pie_chart_alcaldia(capistrano_total, competencia_total):
    # Verificar si ambos valores son cero para evitar problemas en la gráfica
    if capistrano_total == 0 and competencia_total == 0:
        capistrano_total = 1  # Evitar división por cero colocando un valor mínimo
        competencia_total = 1

    # Datos para la gráfica
    labels = ['Capistrano', 'Competencia']
    sizes = [capistrano_total, competencia_total]
    colors = ['#009975', '#FF5733']

    # Crear la figura y el eje
    fig, ax = plt.subplots()

    # Crear la gráfica circular
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)

    # Asegurar que el gráfico sea un círculo
    ax.axis('equal')

    # Título de la gráfica
    ax.set_title('Distribución de Capistrano vs Competencia')

    # Ajustar el diseño para evitar superposiciones
    plt.tight_layout()

    # Cambiar el tamaño y color de los porcentajes
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(22)

    # Convertir la gráfica a imagen base64
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_str_pie_alcaldia = base64.b64encode(buffer.getvalue()).decode()
    plt.close()  # Cerrar la gráfica para liberar memoria

    return img_str_pie_alcaldia