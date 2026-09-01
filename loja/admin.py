from django.contrib import admin
from .models import Categoria, ItemAdicional, GrupoOpcao, Produto, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'ativo')

@admin.register(ItemAdicional)
class ItemAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco')

@admin.register(GrupoOpcao)
class GrupoOpcaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'qtd_minima', 'qtd_maxima')
    filter_horizontal = ('itens',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_base', 'ativo')
    filter_horizontal = ('grupos_opcoes',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_cliente', 'telefone_cliente', 'valor_total', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
