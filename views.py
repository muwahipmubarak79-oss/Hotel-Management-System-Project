
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category, MenuItem, Order, OrderItem
import json

def restaurant_home(request):
    """Muuqaalka guud ee maqaayadda"""
    categories = Category.objects.all()
    menu_items = MenuItem.objects.filter(is_available=True)
    return render(request, 'restaurant/home.html', {
        'categories': categories,
        'menu_items': menu_items
    })

@csrf_exempt # Tani waa kumeel gaar si loogu tijaabiyo JavaScript-kaaga
def contact_api(request):
    """Xallinta ciladda 404 ee /api/contact"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Halkan waxaad ku keydin kartaa fariinta haddii aad leedahay Contact Model
            print(f"Fariin cusub: {data}") 
            return JsonResponse({"message": "Waad ku mahadsantahay xiriirkaaga!"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def place_order_api(request):
    """Aqbalidda dalabaadka cuntada"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 1. Samee Order-ka weyn
            order = Order.objects.create(
                customer_name=data.get('name'),
                customer_email=data.get('email'),
                customer_phone=data.get('phone'),
                total_price=data.get('total', 0)
            )
            
            # 2. Ku dar cuntooyinka la doortay (haddii ay ku jiraan xogta)
            # Tani waxay u baahan tahay in frontend-ka laga soo diro liiska 'items'
            
            return JsonResponse({"message": "Dalabkaaga waa la helay!", "order_id": order.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Method not allowed"}, status=405)

