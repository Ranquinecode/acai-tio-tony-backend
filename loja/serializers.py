from rest_framework import serializers
from .models import Categoria, ItemAdicional, GrupoOpcao, ItemGrupoOpcao, Produto, Pedido


class ItemAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemAdicional
        fields = ['id', 'nome', 'imagem_url']


class ItemGrupoOpcaoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='item.id')
    nome = serializers.ReadOnlyField(source='item.nome')
    imagem_url = serializers.ReadOnlyField(source='item.imagem_url')
    preco = serializers.DecimalField(source='preco_especifico', max_digits=6, decimal_places=2)
    # Recursão para expor os grupos filhos (condicionais) que abrem ao selecionar este item
    grupos_filhos = serializers.SerializerMethodNested(read_only=True)

    class Meta:
        model = ItemGrupoOpcao
        fields = ['id', 'nome', 'imagem_url', 'preco', 'grupos_filhos']

    def get_grupos_filhos(self, obj):
        # Evita importação circular e renderiza os subgrupos
        serializer = GrupoOpcaoSerializer(obj.grupos_filhos.all(), many=True, context=self.context)
        return serializer.data


class GrupoOpcaoSerializer(serializers.ModelSerializer):
    itens = ItemGrupoOpcaoSerializer(source='itens_relacionados', many=True, read_only=True)

    class Meta:
        model = GrupoOpcao
        fields = [
            'id', 
            'nome', 
            'qtd_minima', 
            'qtd_maxima', 
            'permitir_repeticao',
            'permitir_exceder', 
            'preco_item_excedente', 
            'limite_excedente', 
            'itens'
        ]


class ProdutoSerializer(serializers.ModelSerializer):
    grupos_opcoes = GrupoOpcaoSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = [
            'id', 
            'categoria', 
            'nome', 
            'descricao', 
            'preco_base', 
            'preco_camada_extra', 
            'eh_customizavel', 
            'eh_combo', 
            'grupos_opcoes', 
            'imagem_url', 
            'ativo'
        ]


class CategoriaSerializer(serializers.ModelSerializer):
    produtos = ProdutoSerializer(many=True, read_only=True)

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'ordem', 'ativo', 'produtos']


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
