from django.shortcuts import render
from .models import EnergyConsumption

def energy_dashboard(request):
    energy_data = EnergyConsumption.objects.select_related('appliance').order_by('-timestamp')[:10]
    return render(request, 'energy_meter.html', {'energy_data': energy_data})
