from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import max_reservas
from .forms import CreateUserForm



def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nickname = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=nickname, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, F"Bienvenido {nickname}")
                return redirect("flights")
            else:
                messages.error(request, "Los datos son incorrectos")
        else:
            messages.error(request, "Los datos son incorrectos")
    form = AuthenticationForm()
    titulo = "Acceder"
    return render(request, "login.html", {"form": form, "titulo": titulo})

class ViewRegister(View):
    def get(self, request):
        form = CreateUserForm()
        titulo = "Registro"

        return render(request, "registration.html", {"form": form, "titulo": titulo})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            name_user = form.cleaned_data.get("username")
            messages.success(request, F"Bienvenid@ a TuluaYork Airlines {name_user}")
            login(request, user)
            max = max_reservas(cantidad=2, user=user)
            max.save()
            return redirect("flights")
        else: 
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            titulo = "Registro"
            return render(request, "registration.html", {"form": form, "titulo": titulo})

def getout(request):
    logout(request)
    messages.success(request, F"Tu sesion se ha cerrado")
    return redirect("flights")

def perfil(request, user_id):
    # Recuperamos la instancia de la persona
    instancia = User.objects.get(id=user_id)

    # Creamos el formulario con los datos de la instancia
    form = CreateUserForm(instance=instancia)

    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Actualizamos el formulario con los datos recibidos
        form = CreateUserForm(request.POST, instance=instancia)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            login(request, instancia)
            messages.success(request, F"Los datos han sido actualizados con exito")

    # Si llegamos al final renderizamos el formulario
    titulo = "Actualizar perfil"
    return render(request, "profile.html", {'form': form, 'titulo': titulo})