from django.urls import path
from . import views

app_name= 'reservas'

urlpatterns = [
    path('recorrido/<int:pk>/', views.detalle_recorrido, name="detalle_recorrido"),
    path('gestionar_recorridos/', views.agregar_recorrido, name="agregar_recorrido"),
    path('recorrido/<int:pk>/eliminar/', views.eliminar_recorrido, name="eliminar_recorrido"),
    path('recorrido/<int:pk>/editar/', views.editar_recorrido, name="editar_recorrido"),
    path('puntos_turisticos/', views.agregar_punto, name="agregar_punto"),

]