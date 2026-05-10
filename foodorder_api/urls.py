# URLs principales del proyecto
from django.urls import path, include

urlpatterns = [
    path('api/', include('restaurant.urls')),
]