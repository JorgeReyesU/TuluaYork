from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

def perfil(request):
    titulo = ""
    return render(request, "profile.html")

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
                messages.success(request, "Los datos son incorrectos")
        else:
            messages.success(request, "Los datos son incorrectos")
    form = AuthenticationForm()
    titulo = "Acceder"
    return render(request, "login.html", {"form": form, "titulo": titulo})

class ViewRegister(View):
    def get(self, request):
        form = UserCreationForm()
        titulo = "Registro"
        return render(request, "registration.html", {"form": form, "titulo": titulo})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            name_user = form.cleaned_data.get("username")
            messages.success(request, F"Bienvenid@ a TuluaYork Airlines {name_user}")
            login(request, user)
            return redirect("flights")
        else: 
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "registration.html", {"form": form, "titulo": titulo})

def getout(request):
    logout(request)
    messages.success(request, F"Tu sesion se ha cerrado")
    return redirect("flights")