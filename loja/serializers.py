from rest_framework import serializers
from .models import (
    Categoria, 
    CategoriaItemAdicional,
    ItemAdicional, 
    GrupoOpcao, 
    ItemGrupoOpcao, 
    Produto, 
    Pedido, 
    ItemCombo
)


class CategoriaItemAdicionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaItemAdicional
        fields = ['id', 'nome', 'ordem']


class ItemAdicionalSerializer(serializers.ModelSerializer):
    categoria_item = CategoriaItemAdicionalSerializer(read_only=True)

    class Meta:
        model = ItemAdicional
        fields = ['id', 'nome', 'categoria_item', 'disponibilidade', 'imagem_url']


class ItemGrupoOpcaoSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='item.id')
    nome = serializers.ReadOnlyField(source='item.nome')
    disponibilidade = serializers.ReadOnlyField(source='item.disponibilidade')
    imagem_url = serializers.ReadOnlyField(source='item.imagem_url')
    categoria_item = CategoriaItemAdicionalSerializer(source='item.categoria_item', read_only=True)
    preco = serializers.DecimalField(source='preco_especifico', max_digits=6, decimal_places=2)
    grupos_filhos = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ItemGrupoOpcao
        fields = ['id', 'nome', 'categoria_item', 'disponibilidade', 'imagem_url', 'preco', 'ordem', 'grupos_filhos']

    def get_grupos_filhos(self, obj):
        # Evita importação circular e renderiza os subgrupos filhos ordenados
        serializer = GrupoOpcaoSerializer(
            obj.grupos_filhos.all().order_by('nome'), 
            many=True, 
            context=self.context
        )
        return serializer.data


class GrupoOpcaoSerializer(serializers.ModelSerializer):
    itens = serializers.SerializerMethodField()

    class Meta:
        model = GrupoOpcao
        fields = [
            'id', 
            'nome', 
            'qtd_minima', 
            'qtd_maxima', 
            'permitir_repeticao',
            'cobrar_camada_extra',
            'permitir_exceder', 
            'preco_item_excedente', 
            'limite_excedente', 
            'itens'
        ]

    def get_itens(self, obj):
        # Filtra itens ocultos no estoque e aplica a ordenação cadastrada
        queryset = obj.itens_relacionados.exclude(item__disponibilidade='oculto').order_by('ordem')
        return ItemGrupoOpcaoSerializer(queryset, many=True, context=self.context).data


class ItemComboSerializer(serializers.ModelSerializer):
    produto_conteudo = serializers.SerializerMethodField()

    class Meta:
        model = ItemCombo
        fields = ['id', 'quantidade', 'ordem', 'produto_conteudo']

    def get_produto_conteudo(self, obj):
        if obj.produto_conteudo:
            return ProdutoSerializer(obj.produto_conteudo, context=self.context).data
        return None


class ProdutoSerializer(serializers.ModelSerializer):
    grupos_opcoes = serializers.SerializerMethodField()
    itens_combo = serializers.SerializerMethodField()

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
            'itens_combo',
            'imagem_url', 
            'ativo'
        ]

    def get_grupos_opcoes(self, obj):
        # Busca a ordenação exata dos grupos atribuída especificamente para este produto
        if hasattr(obj, 'produtogrupoopcao_set'):
            relacoes = obj.produtogrupoopcao_set.select_related('grupo_opcao').order_by('ordem')
            grupos = [rel.grupo_opcao for rel in relacoes]
        elif hasattr(obj, 'produto_grupos'):
            relacoes = obj.produto_grupos.select_related('grupo_opcao').order_by('ordem')
            grupos = [rel.grupo_opcao for rel in relacoes]
        else:
            grupos = obj.grupos_opcoes.all()
        return GrupoOpcaoSerializer(grupos, many=True, context=self.context).data

    def get_itens_combo(self, obj):
        queryset = obj.itens_combo.order_by('ordem')
        return ItemComboSerializer(queryset, many=True, context=self.context).data


class CategoriaSerializer(serializers.ModelSerializer):
    produtos = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ['id', 'nome', 'ordem', 'ativo', 'produtos']

    def get_produtos(self, obj):
        # Retorna apenas os produtos ativos da categoria
        queryset = obj.produtos.filter(ativo=True)
        return ProdutoSerializer(queryset, many=True, context=self.context).data


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
