
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Hubi in ciwaankani uu yahay midka JavaScript-kaagu u yeerayo
    path('api/contact/', views.contact_api, name='contact_api'),
]