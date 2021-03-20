from django.shortcuts import render
from flights.models import vuelo, ciudad

from datetime import date
from datetime import datetime
#Día actual
today = date.today()
#Fecha actual
now = datetime.now()

# --------------------------------------------------------------
def flights(request):
    titulo = "Inicio"
    mensaje = ""
    ciudades = ciudad.objects.all()
    return render(request, "vuelos.html", {"titulo": titulo, "mensaje": mensaje, "ciudades": ciudades})

def findflights(request, ciudad1_name, ciudad2_name):
    titulo = "Encontrar vuelos"
    mensaje = ""

    allciu = ciudad.objects.all()
    ciudad1_id = 0
    ciudad2_id = 0

    for i in range(len(allciu)):
        if ciudad1_name == allciu[i].nombre:
            ciudad1_id = allciu[i]
        if ciudad2_name == allciu[i].nombre:
            ciudad2_id = allciu[i]




    return render(request, "findvuelos.html", {"titulo": titulo, "mensaje": mensaje, "ciudad1": ciudad1_id, "ciudad2": ciudad2_id})