from django.urls import path
from .views import upload_image, home, maps,planogram
from .utils.dinamicList import dinamic_list
from .utils.geolocation import get_markers_alcaldia, get_markers

urlpatterns = [
    path('upload', upload_image, name='upload_image'),  # Ruta para la vista upload_image
    path('', dinamic_list, name='dinamic_list'), # Ruta para la vista my_view
    path('home', home, name='home'),  # Página principal
    path('planogram', planogram, name='planogram'),  # Página de Planograma
    path('maps', maps, name='maps'),
    path('api/markers/', get_markers, name='get_markers'),
    path('getmarkers/', get_markers_alcaldia, name='get_markers_alcaldia'),

]