
from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Hubi in 'user' uu ka mid yahay fields-ka ku jira Model-ka Order.
    # Haddii model-kaagu u isticmaalo 'customer', halkaan u bedel 'customer'
    list_display = ['id', 'user', 'total_price', 'status', 'created_at'] 
    
    # Haddii aadan hubin magacyada, waxaad halkan ku koobi kartaa kaliya ID:
    # list_display = ['id', 'status']
