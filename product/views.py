import os
from pathlib import Path
from django.shortcuts import render
from django.db.models import Max
from django.utils.timezone import now
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from .utils.graficalOptions import create_chart
from .utils.geolocation import  get_markers, get_markers_alcaldia
from product.models import Alcaldia, Sucursales, Prediccion
from .utils.imageProcessData import (
    read_image, convert_image_to_bytes, draw_boxes_on_image, convert_image_to_base64
)
from .utils.prediction import make_prediction, filter_predictions
# Claves de Azure Custom Vision
PREDICTION_KEY = os.getenv('PREDICTION_KEY')
ENDPOINT = os.getenv('ENDPOINT')
PROJECT_ID = os.getenv('PROJECT_ID')
PUBLISH_ITERATION_NAME = os.getenv('PUBLISH_ITERATION_NAME')
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

def upload_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        try:
            # Procesamiento de la imagen
            image_file = request.FILES['image']
            image = read_image(image_file)
            image_bytes = convert_image_to_bytes(image)

            # Predicción
            results = make_prediction(predictor, PROJECT_ID, PUBLISH_ITERATION_NAME, image_bytes)
            valid_predictions = filter_predictions(results.predictions)

             # Agrupar predicciones por fecha
            today_date = now().strftime("%d/%m/%Y")  # Fecha actual en formato dd/mm/yyyy
            data = {
                today_date: {
                    'capistrano': 0,
                    'lala': 0,
                    'san rafael': 0,
                    'fud': 0,
                    'villita': 0,
                    'zwan': 0,
                    'bafar': 0,
                    'chimex': 0,
                    'kir': 0,
                    'sabori': 0,
                }
            }

            for pred in valid_predictions:
                if pred.tag_name == "capistrano":
                    data[today_date]['capistrano'] += 1
                elif pred.tag_name == "lala":
                    data[today_date]['lala'] += 1
                elif pred.tag_name == "san rafael":
                    data[today_date]['san rafael'] += 1
                elif pred.tag_name == "fud":
                    data[today_date]['fud'] += 1
                elif pred.tag_name == "villita":
                    data[today_date]['villita'] += 1
                elif pred.tag_name == "zwan":
                    data[today_date]['zwan'] += 1
                elif pred.tag_name == "bafar":
                    data[today_date]["bafar"] += 1
                elif pred.tag_name == "chimex":
                    data[today_date]["chimex"] += 1
                elif pred.tag_name == "kir":
                    data[today_date]["kir"] += 1
                elif pred.tag_name == "sabori":
                    data[today_date]["sabori"] += 1

            chart_image = create_chart(data[today_date]) 

            # Dibujar recuadros en la imagen
            image_with_boxes = draw_boxes_on_image(image, valid_predictions)
            img_str = convert_image_to_base64(image_with_boxes)

            # Calcular estadísticas
            total_products = len(valid_predictions)
            capistrano_count = sum(1 for pred in valid_predictions if pred.tag_name == "capistrano")
            lala_count = sum(1 for pred in valid_predictions if pred.tag_name == "lala")
            san_rafael_count = sum(1 for pred in valid_predictions if pred.tag_name == "san rafael")
            fud_count = sum(1 for pred in valid_predictions if pred.tag_name == "fud")
            villita_count = sum(1 for pred in valid_predictions if pred.tag_name == "villita")
            zwan_count = sum(1 for pred in valid_predictions if pred.tag_name == "zwan")
            bafar_count = sum(1 for pred in valid_predictions if pred.tag_name == "bafar")
            chimex_count = sum(1 for pred in valid_predictions if pred.tag_name == "chimex")
            kir_count = sum(1 for pred in valid_predictions if pred.tag_name == "kir")
            sabori_count = sum(1 for pred in valid_predictions if pred.tag_name == "sabori")

            # Datos de la solicitud
            nombre_sucursal = request.POST.get('sucursal')
            id_alcaldias = request.POST.get('alcaldia')
            id_cadena = request.POST.get('cadena')
            direccion = request.POST.get('address')
            latitud = request.POST.get('latitude')
            longitud = request.POST.get('longitude')

            # Verificar que latitud y longitud no sean nulos
            if not latitud or not longitud:
                return render(request, 'userUploadimage.html', {'error': 'Las coordenadas son inválidas.'})

            sucursal_existente_por_nombre = Sucursales.objects.filter(name_branch=nombre_sucursal).first()

                # Verificar si la sucursal ya existe por nombre
            if sucursal_existente_por_nombre:
                    # Si existe, regresar a la vista con el valor de la sucursal existente
                    return render(request, 'userUploadimage.html', {
                        'error': 'Ya existe una sucursal con ese nombre.',
                        'sucursal_existente': sucursal_existente_por_nombre  # Retornar la sucursal existente
                    })

                # Si no existe, crear una nueva sucursal
            ultimo_id = Sucursales.objects.aggregate(max_id=Max('id_branch'))['max_id']

                # Asignar el nuevo ID consecutivo
            if ultimo_id is None:
                    id_sucursal = 1  # Si no hay registros, asignar el primer ID
            else:
                    id_sucursal = ultimo_id + 1  # Asignar el siguiente ID

            # Crear la nueva sucursal
            sucursal = Sucursales(
                id_branch=id_sucursal,
                name_branch=nombre_sucursal,
                direccion=direccion,
                latitud=latitud,
                longitud=longitud
            )
            sucursal.save()  # Guardar la nueva sucursal

            try:

                # Guardar los resultados en la base de datos
                prediccion = Prediccion.objects.create(
                    id_branch=sucursal,  # Usa el objeto sucursal completo
                    id_alcaldia=id_alcaldias,
                    id_chain = id_cadena,
                    cantidad_capistrano=capistrano_count,
                    cantidad_lala=lala_count,
                    cantidad_san_rafael=san_rafael_count,
                    cantidad_fud=fud_count,
                    cantidad_villita=villita_count,
                    cantidad_zwan=zwan_count,
                    cantidad_bafar=bafar_count,
                    cantidad_chimex=chimex_count,
                    cantidad_kir=kir_count,
                    cantidad_sabori=sabori_count,
                    total_productos=total_products,
                )
                print(f"Prediccion creada con éxito: {prediccion}")
            except Exception as e:
                print(f"Error al crear la prediccion: {e}")

            # Pasar los datos al contexto
            context = {
                'sucursal': nombre_sucursal,
                'img_str': img_str,
                'latitud': latitud,
                'longitud': longitud,
                'chart_image': chart_image,
                'direccion': direccion,
                'date': today_date,


            }

            return render(request, 'adminGraficalDash.html', context)
        except Alcaldia.DoesNotExist:
            return render(request, 'userUploadimage.html', {'error': 'Alcaldía no encontrada.'})
        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'userUploadimage.html', {'error': 'Ocurrió un error procesando la imagen.'})

    return render(request, 'userUploadimage.html')

def home(request):

    return render(request, 'adminGraficalDash.html')  # Renderiza la plantilla home.html
def settings(request):
    return render(request, 'settings.html')  # Renderiza la plantilla settings.html

def planogram(request):
    # Llama a get_markers para obtener los marcadores
    markers = get_markers(request)

    # Puedes pasar los marcadores a la plantilla si lo necesitas
    context = {
        'markers': markers,
    }

    return render(request, 'mapaSucursales.html', context)  # Renderiza la plantilla mapaSucursales.html

def maps(request):
    # Llama a get_markers_alcaldia para obtener los marcadores de alcaldía
    alcaldia_markers = get_markers_alcaldia(request)

    # Puedes pasar los marcadores a la plantilla si lo necesitas
    context = {
        'alcaldia_markers': alcaldia_markers,
    }

    return render(request, 'mapasAlcaldia.html', context)  # Renderiza la plantilla mapasAlcaldia.html

