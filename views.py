from django.shortcuts import render
from django.http import JsonResponse
import json

def home(request):
   
    return render(request, 'home.html')

def contact_api(request):
   
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"New data: {data}")
            return JsonResponse({"status": "success", "message": "Your message has been received!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)