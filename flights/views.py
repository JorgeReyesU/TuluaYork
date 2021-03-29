from django.shortcuts import render, redirect
from flights.models import vuelo, ciudad, reserva
from django.contrib.auth.models import User
from authentication.models import max_reservas
from .forms import vueloForm, reservaForm
from django.contrib import messages

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
    context = {"titulo": titulo, "mensaje": mensaje, "ciudades": ciudades}

    if request.method == 'POST':
        print(request.POST)
        return redirect(findflights, ciudad1_name=request.POST.get('input1'), ciudad2_name=request.POST.get('input2'))
    return render(request, "vuelos.html", context)

def findflights(request, ciudad1_name, ciudad2_name):
    titulo = "Encontrar vuelos"
    mensaje = ""

    ciudad1 = ciudad.objects.get(nombre=ciudad1_name)#, pais="Inglaterra")
    ciudad2 = ciudad.objects.get(nombre=ciudad2_name)

    vuelos = vuelo.objects.filter(origen=ciudad1,destino=ciudad2)
    print(vuelos)

    context = {"titulo": titulo, "mensaje": mensaje, "ciudad1": ciudad1, "ciudad2": ciudad2, "vuelos": vuelos}

    return render(request, "findvuelos.html", context)

def gvuelos(request):
    titulo = "Gestionar vuelos"
    mensaje = ""

    vuelos = vuelo.objects.filter(fecha_salida__gte=today) # lt, gt, lte, gte

    print(vuelos)
    context = {"titulo": titulo, "mensaje": mensaje, "vuelos": vuelos}
    return render(request, "Gvuelos.html", context)

def createflight(request):
    titulo = "Crear vuelo"
    mensaje = ""
    form = vueloForm()

    if  request.method == 'POST':
        #print('Printing post:', request.post)
        form = vueloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/flights/gvuelos')

    context = {"titulo": titulo, "mensaje": mensaje,"form": form}
    return render(request, "create_vuelo.html", context)

def updateflight(request, vuelo_id):
    titulo = "Actualizar vuelo"
    mensaje = ""

    Vuelo = vuelo.objects.get(id=vuelo_id)
    form = vueloForm(instance=Vuelo)

    if  request.method == 'POST':
        #print('Printing post:', request.post)
        form = vueloForm(request.POST, instance=Vuelo)
        if form.is_valid():
            form.save()
            return redirect('/flights/gvuelos')

    context = {"titulo": titulo, "mensaje": mensaje,"form": form}
    return render(request, "create_vuelo.html", context)

def cancelflight(request, vuelo_id):
    titulo = "Cancelar vuelo"
    mensaje = ""

    Vuelo = vuelo.objects.get(id=vuelo_id)

    if request.method == 'POST':
        if vuelo.estado == True:
            Vuelo.estado = False
            Vuelo.save()
            reservas = reserva.objects.filter(vuelo=Vuelo).distinct('usuario')
            for Reserva in reservas:
                Reserva.usuario.max_vuelos += 1
                Reserva.save()
            return redirect('/flights/gvuelos')

    context = {"titulo": titulo, "mensaje": mensaje, "vuelo": Vuelo}
    return render(request, "cancel_vuelo.html", context)

def greservas(request, user_id):
    titulo = "Mis reservas"
    mensaje = ""

    reservas = reserva.objects.filter(usuario=user_id, estado=True, vuelo__fecha_salida__gte=today) # lt, gt, lte, gte
    max = max_reservas.objects.get(user=user_id)

    context = {"titulo": titulo, "mensaje": mensaje, "reservas": reservas, 'max': max}
    return render(request, "mis_vuelos.html", context)

def cancelreserve(request, reserva_id):
    titulo = "Cancelar reserva"
    mensaje = ""

    Reserva = reserva.objects.get(id=reserva_id)
    Vuelo = vuelo.objects.get(id=Reserva.vuelo.id)

    if request.method == 'POST':
        if Reserva.estado == True:
            Reserva.estado = False
            Reserva.save()
            Vuelo.capacidad += 1
            Vuelo.save()
            return redirect('/flights/greservas/'+ str(Reserva.usuario.id))

    context = {"titulo": titulo, "mensaje": mensaje, "reserva": Reserva}
    return render(request, "cancel_reserva.html", context)

def reserveflight(request, user_id, vuelo_id):
    titulo = "Reservar vuelo"
    mensaje = ""

    user = User.objects.get(id=user_id)
    Vuelo = vuelo.objects.get(id=vuelo_id)
    Vuelos = vuelo.objects.filter(fecha_salida__gte=today)

    max = max_reservas.objects.get(user=user_id)
    reservas = reserva.objects.filter(usuario=user_id, vuelo__fecha_salida__gte=today)

    form = reservaForm()

    if  request.method == 'POST':
        if len(reservas) < max.cantidad:
            form = reservaForm(request.POST, instance=reserva(vuelo=Vuelo, usuario=user))
            if form.is_valid():
                form.save()
                return redirect('/flights/greservas/'+ str(user_id))
        else:
            messages.error(request, F"Ya reservaste tu maximo")

    context = {"titulo": titulo, "mensaje": mensaje,"form": form, "vuelo": Vuelo, "Vuelos": Vuelos, "max": max}

    return render(request, "reservar_vuelo.html", context)

#href="/flights/findflights/inputGroupSelect01/inputGroupSelect02"