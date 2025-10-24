"""
URL configuration for citytur_catamarca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render,redirect
from apps.reservas import views as reservas_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', lambda request: render(request, 'reservas/inicio.html'), name='inicio'),
    path('', lambda request: render(request, 'reservas/inicio.html')),
    path('reserva/', lambda request: redirect('reservas:reservas_crear'), name='reserva_directa'),

    path('gestion_recorridos/', lambda request: redirect('reservas:agregar_recorrido'), name='gestion_directa'),
    path('reservas/', include('apps.reservas.urls'))
]
