from django.urls import path
from .views import get_latest_data

urlpatterns = [
    path('latest/', get_latest_data, name='get_latest_data'),
]