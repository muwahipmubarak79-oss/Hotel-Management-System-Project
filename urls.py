
from django.contrib import admin
from django.urls import path
from . import views  # Hubi inuu halkaan ku jiro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('api/contact/', views.contact_api, name='contact_api'),
]
