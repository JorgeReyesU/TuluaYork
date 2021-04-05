from django.shortcuts import render, redirect
from flights.models import vuelo, ciudad, reserva, interface_vacuna, interface_impuesto
from django.contrib.auth.models import User
from authentication.models import max_reservas
from .forms import vueloForm, reservaForm
from django.contrib import messages
import requests as rq
import yagmail
import numpy as np

from datetime import date, datetime, timedelta
#Día actual
today = date.today()
tomorrow = today + timedelta(days=1)
#Fecha actual
now = datetime.now()

# --------------------------------------------------------------
def flights(request):
    titulo = "Inicio"
    mensaje = ""
    ciudades = ciudad.objects.all()
    
    if True == False:
        reservas = reserva.objects.filter(estado=True, vuelo__fecha_salida=tomorrow)
        email = yagmail.SMTP('tuluayork.info.vuelo@gmail.com', "R3d3s2021")
        for Reserva in reservas:
            contenido = "El vuelo " + Reserva.vuelo.nombre + " con destino a la ciudad de " + Reserva.vuelo.destino.nombre + " para el dia de mañana " + tomorrow.strftime("%m/%d/%Y") + " con hora " + Reserva.vuelo.hora_salida.strftime("%H:%M %p") + " te esta esperando, esperamos tengas un buen viaje."
            email.send(to=Reserva.usuario.email, subject="Recordatorio de vuelo - TuluaYork Airlines", contents=[contenido])

    if request.method == 'POST':
        print(request.POST)
        return redirect(findflights, ciudad1_name=request.POST.get('input1'), ciudad2_name=request.POST.get('input2'))

    context = {"titulo": titulo, "mensaje": mensaje, "ciudades": ciudades}
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

    vuelos = vuelo.objects.filter(fecha_salida__gte=today, estado=True) # lt, gt, lte, gte

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
        if Vuelo.estado == True:
            Vuelo.estado = False
            Vuelo.save()
            #Reservas = reserva.objects.filter(vuelo=Vuelo).values_list('usuario_id', flat=True).distinct()
            Reservas = reserva.objects.filter(vuelo=Vuelo, estado=True)
            for Reserva in Reservas:
                Max_reserva = max_reservas.objects.get(user_id=Reserva.usuario.id)
                Max_reserva.cantidad += 1
                Max_reserva.save()
                Reserva.estado = False
                Reserva.save()
            return redirect('/flights/gvuelos')

    context = {"titulo": titulo, "mensaje": mensaje, "vuelo": Vuelo}
    return render(request, "cancel_vuelo.html", context)

def greservas(request, user_id):
    titulo = "Mis reservas"
    mensaje = ""

    reservas = reserva.objects.filter(usuario=user_id, estado=True, vuelo__fecha_salida__gte=today) # lt, gt, lte, gte
    max = max_reservas.objects.get(user=user_id)

    reservasW = reserva.objects.filter(usuario=user_id, estado=True, vuelo__fecha_salida=today)

    climas = [None] * len(reservasW)
    for i in range(len(reservasW)):
        climas[i] = [None] * 3

    for i in range(len(reservasW)):
        city = reservasW[i].vuelo.destino.nombre
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid=28db4062029546869583fb2f6642acb5&units=metric'.format(
            city)
        res = rq.get(url)
        data = res.json()
        climas[i][0] = city
        climas[i][1] = data['main']['temp']
        climas[i][2] = data['weather'][0]['description']

    context = {"titulo": titulo, "mensaje": mensaje, "reservas": reservas, 'max': max, 'climas': climas, 'n': len(climas)}
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

    Destino = ciudad.objects.get(id=Vuelo.destino.id)
    inVacs = interface_vacuna.objects.filter(destino=Destino.id)
    inImps = interface_impuesto.objects.filter(destino=Destino.id)


    form = reservaForm()

    if  request.method == 'POST':
        if len(reservas) < max.cantidad:
            form = reservaForm(request.POST, instance=reserva(vuelo=Vuelo, usuario=user))
            if form.is_valid():
                form.save()
                Vuelo.capacidad -= 1
                Vuelo.save()
                return redirect('/flights/greservas/'+ str(user_id))
        else:
            messages.error(request, F"Ya reservaste tu maximo")

    context = {"titulo": titulo, "mensaje": mensaje,"form": form, "vuelo": Vuelo, "Vuelos": Vuelos, "max": max, "inVacs": inVacs, "inImps": inImps}

    return render(request, "reservar_vuelo.html", context)

#href="/flights/findflights/inputGroupSelect01/inputGroupSelect02"