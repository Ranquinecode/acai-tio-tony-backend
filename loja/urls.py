from django.urls import path
from django.http import JsonResponse

def status_api(request):
    return JsonResponse({"status": "API Ativa", "versao": "1.0"})

urlpatterns = [
    path('', status_api),
]
