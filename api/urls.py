from django.urls import include, path
from rest_framework import routers

from api.views import WeatherApiViewset

router = routers.DefaultRouter()
router.register('', WeatherApiViewset, basename="weather-api")

urlpatterns = [
    # DRF views
    path('', include(router.urls)),
]
