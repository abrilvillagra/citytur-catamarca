from django.urls import path
from . import views

app_name = 'informes'

urlpatterns = [
    path('', views.panel_informes, name='panel_informes'),
    path('recorridos_activos/pdf/', views.RecorridosActivosPDF.as_view(), name='recorridos_activos_pdf'),
    path('reservas_por_recorrido/pdf/', views.ReservasPorRecorridoPDF.as_view(), name='reservas_por_recorrido_pdf'),
    path('estadisticas_pasajeros/pdf/', views.EstadisticasPasajerosPDF.as_view(), name='estadisticas_pasajeros_pdf'),
    path('reservas_por_fecha/', views.panel_informes, name='reservas_por_fecha'),
]
