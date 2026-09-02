from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Painel de Administração Jazzmin
    path('admin/', admin.site.urls),
    
    # Endpoints da API REST (Categorias, Produtos, Pedidos, Healthcheck)
    path('api/', include('loja.urls')),
    
    # Redirecionamento amigável da raiz para os endpoints da loja (opcional, garante resposta rápida)
    path('', include('loja.urls')),
]
