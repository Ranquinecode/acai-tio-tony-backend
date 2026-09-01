from rest_framework import serializers
from .models import Categoria, ItemAdicional, GrupoOpcao, Produto, Pedido

class ItemAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAdicional
        fields = ['id', 'nome', 'preco']


class GrupoOpcaoSerializer(serializers.ModelSerializer):
    itens = ItemAdicionalSerializer(many=True, read_only=True)

    class Meta:
        model = GrupoOpcao
        fields = ['id', 'nome', 'qtd_minima', 'qtd_maxima', 'itens']


class ProdutoSerializer(serializers.ModelSerializer):
    grupos_opcoes = GrupoOpcaoSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'categoria', 'nome', 'preco_base', 'preco_camada_extra', 'grupos_opcoes', 'imagem_url', 'ativo']


class CategoriaSerializer(serializers.ModelSerializer):
    produtos = ProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'ordem', 'ativo', 'produtos']


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
