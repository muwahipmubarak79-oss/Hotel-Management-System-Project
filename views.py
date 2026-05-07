
import json
from django.http import JsonResponse
from .models import ContactMessage

def contact_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Tani waa qaybta ugu muhiimsan ee kaydinta
            ContactMessage.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                subject=data.get('subject'),
                message=data.get('message')
            )
            return JsonResponse({"status": "success", "message": "Fariinta waa la keydiyay!"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=405)

