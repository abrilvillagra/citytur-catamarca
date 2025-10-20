from django.urls import path
from . import views

app_name= 'reservas'

urlpatterns = [
    path('gestionar_recorridos/', views.agregar_recorrido, name="agregar_recorrido"),
]