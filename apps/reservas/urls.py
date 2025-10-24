from django.urls import path
from . import views

app_name= 'reservas'

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('gestionar_recorridos/', views.agregar_recorrido, name="agregar_recorrido"),
    path('nueva/', views.crear_reserva, name='reservas_crear'),

]