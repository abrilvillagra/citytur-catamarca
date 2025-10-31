from django.urls import path
from . import views

app_name = 'reservas'

urlpatterns = [
    # Inicio
    path('inicio/', views.inicio, name='inicio'),

    # Recorridos
    path('gestionar_recorridos/', views.agregar_recorrido, name="agregar_recorrido"),
    path('recorrido/<int:pk>/', views.detalle_recorrido, name="detalle_recorrido"),
    path('recorrido/<int:pk>/editar/', views.editar_recorrido, name="editar_recorrido"),
    path('recorrido/<int:pk>/eliminar/', views.eliminar_recorrido, name="eliminar_recorrido"),

    # Reservas
    path('nueva/', views.crear_reserva, name='reservas_crear'),
    path('listar/', views.listar_reservas, name='listar_reservas'),
    path('editar/<int:id>/', views.editar_reserva, name='editar_reserva'),
    path('cancelar/<int:id>/', views.cancelar_reserva, name='cancelar_reserva'),
]
