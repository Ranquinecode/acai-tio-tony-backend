from django.contrib import admin
from .models import Categoria, ItemAdicional, GrupoOpcao, Produto, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'ativo')
    list_editable = ('ordem', 'ativo')
    search_fields = ('nome',)


@admin.register(ItemAdicional)
class ItemAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')
    list_editable = ('preco',)
    search_fields = ('nome',)


@admin.register(GrupoOpcao)
class GrupoOpcaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'qtd_minima', 'qtd_maxima')
    filter_horizontal = ('itens',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_base', 'preco_camada_extra', 'ativo')
    list_filter = ('categoria', 'ativo')
    list_editable = ('preco_base', 'preco_camada_extra', 'ativo')
    search_fields = ('nome',)
    filter_horizontal = ('grupos_opcoes',)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_cliente', 'telefone_cliente', 'valor_total', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome_cliente', 'telefone_cliente', 'id')
    readonly_fields = ('criado_em',)
