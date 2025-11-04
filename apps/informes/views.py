from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.reservas.models import Recorrido, Reserva, PuntoTuristico
from wkhtmltopdf.views import PDFTemplateView
from datetime import date

def es_admin(user):
    return user.is_authenticated and user.groups.filter(name='Administrador').exists()


# ==============================
# PANEL GENERAL
# ==============================
@login_required
@user_passes_test(es_admin)
def panel_informes(request):
    from django.db.models import Count, Sum

    # ----- 1. Recorridos activos -----
    recorridos_activos = Recorrido.objects.filter(estado=True)


    # ----- 2. Listado de reservas por recorrido -----
    recorrido_id = request.GET.get('recorrido')
    reservas_recorrido = []
    if recorrido_id:
        reservas_recorrido = Reserva.objects.filter(recorrido_id=recorrido_id)

    # ----- 3. Estadísticas de pasajeros por rango -----
    fecha_desde = request.GET.get('desde')
    fecha_hasta = request.GET.get('hasta')
    estadisticas = []
    if fecha_desde and fecha_hasta:
        try:
            estadisticas = (
                Reserva.objects.filter(fecha_reserva__range=[fecha_desde, fecha_hasta])
                .values('recorrido__nombre')
                .annotate(total_pasajeros=Sum('cantidad_personas'))
                .order_by('-total_pasajeros')
            )
        except ValueError:
            pass

    return render(request, 'informes/panel_informes.html', {
        'recorridos_activos': recorridos_activos,
        'reservas_recorrido': reservas_recorrido,
        'recorridos': Recorrido.objects.all(),  # para el select
        'estadisticas': estadisticas,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    })


# ==============================
# EXPORTAR A PDF
# ==============================
class RecorridosActivosPDF(PDFTemplateView):
    template_name = 'informes/recorridos_activos_pdf.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recorridos'] = Recorrido.objects.filter(estado=True)
        return context



class ReservasPorRecorridoPDF(PDFTemplateView):
    template_name = 'informes/reservas_por_recorrido_pdf.html'
    def get_context_data(self, **kwargs):
        from django.conf import settings
        recorrido_id = self.request.GET.get('recorrido')
        context = super().get_context_data(**kwargs)
        context['reservas'] = Reserva.objects.filter(recorrido_id=recorrido_id)
        context['recorrido'] = Recorrido.objects.filter(id=recorrido_id).first()
        return context


class EstadisticasPasajerosPDF(PDFTemplateView):
    template_name = 'informes/estadisticas_pasajeros_pdf.html'
    def get_context_data(self, **kwargs):
        from django.db.models import Sum
        context = super().get_context_data(**kwargs)
        fecha_desde = self.request.GET.get('desde')
        fecha_hasta = self.request.GET.get('hasta')
        context['estadisticas'] = (
            Reserva.objects.filter(fecha_reserva__range=[fecha_desde, fecha_hasta])
            .values('recorrido__nombre')
            .annotate(total_pasajeros=Sum('cantidad_personas'))
            .order_by('-total_pasajeros')
        )
        context['fecha_desde'] = fecha_desde
        context['fecha_hasta'] = fecha_hasta
        return context
