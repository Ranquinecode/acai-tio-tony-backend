from rest_framework import serializers
from .models import Categoria, ItemAdicional, GrupoOpcao, Produto, Pedido

class ItemAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAdicional
        fields = '__all__'

class GrupoOpcaoSerializer(serializers.ModelSerializer):
    itens = ItemAdicionalSerializer(many=True, read_only=True)

    class Meta:
        model = GrupoOpcao
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    grupos_opcoes = GrupoOpcaoSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
