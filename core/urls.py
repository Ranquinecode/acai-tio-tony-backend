from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def healthcheck(request):
    return JsonResponse({"status": "ok", "loja": "Açaí do Tio Tony"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('healthcheck/', healthcheck),
    path('api/', include('loja.urls')),
]
