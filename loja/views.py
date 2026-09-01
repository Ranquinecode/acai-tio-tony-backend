from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Categoria, ItemAdicional, GrupoOpcao, Produto, Pedido
from .serializers import CategoriaSerializer, ItemAdicionalSerializer, GrupoOpcaoSerializer, ProdutoSerializer, PedidoSerializer

class CategoriaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categoria.objects.filter(ativo=True).order_by('ordem')
    serializer_class = CategoriaSerializer

class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Produto.objects.filter(ativo=True)
    serializer_class = ProdutoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
