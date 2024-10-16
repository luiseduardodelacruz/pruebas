from product.models import Cadena, Alcaldia
from django.shortcuts import render

def dinamic_list(request):
    alcaldias = Alcaldia.objects.all()
    cadenas = Cadena.objects.all()
    selected_alcaldia = request.GET.get('alcaldia')  # or however you determine the selected value
    selected_cadena = request.GET.get('cadena')  # or however you determine the selected value
    return render(request, 'userUploadimage.html', {
        'alcaldias': alcaldias,
        'cadenas': cadenas,
        'selected_alcaldias': selected_alcaldia,
        'selected_cadenas': selected_cadena,
    })