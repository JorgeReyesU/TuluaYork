from django.shortcuts import render

# Create your views here.
def flights(request):
    titulo = "Inicio"
    mensaje = ""

    return render(request, "vuelos.html", {"titulo": titulo, "mensaje": mensaje})