from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Categoria, ItemAdicional, GrupoOpcao, Produto, Pedido
from .serializers import (
    CategoriaSerializer, 
    ItemAdicionalSerializer, 
    GrupoOpcaoSerializer, 
    ProdutoSerializer, 
    PedidoSerializer
)

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    # O prefetch_related carrega produtos e adicionais aninhados sem desacelerar a resposta da API
    queryset = Categoria.objects.filter(ativo=True).prefetch_related(
        'produtos__grupos_opcoes__itens_relacionados__item'
    ).order_by('ordem')
    serializer_class = CategoriaSerializer


class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(ativo=True).prefetch_related(
        'grupos_opcoes__itens_relacionados__item'
    )
    serializer_class = ProdutoSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


@api_view(['GET'])
def healthcheck(request):
    """Endpoint leve para manter a aplicação ativa via Cron-job"""
    return Response({"status": "ok", "message": "Açaí do Tio Tony API Online"})
