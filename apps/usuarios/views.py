
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from apps.usuarios.models import Usuario
# Create your views here.

def register_view(request):
    es_admin = False
    if request.user.is_authenticated:
        es_admin = request.user.groups.filter(name="Administrador").exists()

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            return render(request, "usuarios/register.html", {
                "msj": "Las contraseñas no coinciden",
                "es_admin": es_admin
            })

        if Usuario.objects.filter(username=username).exists():
            return render(request, "usuarios/register.html", {
                "msj": "Ese nombre de usuario ya existe",
                "es_admin": es_admin
            })

        if Usuario.objects.filter(email=email).exists():
            return render(request, "usuarios/register.html", {
                "msj": "Ese correo ya está registrado",
                "es_admin": es_admin
            })

        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        login(request, user)

        return redirect(reverse("reservas:inicio"))

    return render(request, "usuarios/register.html", {
        "es_admin": es_admin
    })


def login_view(request):
    es_admin = False
    if request.user.is_authenticated:
        es_admin = request.user.groups.filter(name="Administrador").exists()

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(reverse('reservas:inicio'))
        else:
            return render(request, "usuarios/login.html", {
                "msj": "Credenciales incorrectas",
                "es_admin": es_admin
            })

    return render(request, "usuarios/login.html", {"es_admin": es_admin})



def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect("usuario:login")

