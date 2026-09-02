from django.contrib import admin
from .models import (
    Categoria, 
    ItemAdicional, 
    GrupoOpcao, 
    ItemGrupoOpcao, 
    Produto, 
    Pedido,
    ItemCombo  # Import do ItemCombo adicionado
)


class ItemGrupoOpcaoInline(admin.StackedInline):
    model = ItemGrupoOpcao
    extra = 1
    autocomplete_fields = ['item']
    filter_horizontal = ('grupos_filhos',)
    verbose_name = "Item"
    verbose_name_plural = "Itens deste Grupo (Com subgrupos opcionais)"
    fields = ('item', 'preco_especifico', 'grupos_filhos')


class ItemComboInline(admin.TabularInline):
    model = ItemCombo
    fk_name = 'combo'
    extra = 1
    verbose_name = "Produto do Combo"
    verbose_name_plural = "Produtos que compõem este Combo"
    autocomplete_fields = ['produto_conteudo']
    fields = ('produto_conteudo', 'quantidade', 'ordem')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'ativo')
    list_editable = ('ordem', 'ativo')
    search_fields = ('nome',)


@admin.register(ItemAdicional)
class ItemAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)


@admin.register(GrupoOpcao)
class GrupoOpcaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'qtd_minima', 
        'qtd_maxima', 
        'permitir_repeticao',
        'permitir_exceder', 
        'preco_item_excedente',
        'limite_excedente'
    )
    list_editable = (
        'qtd_minima', 
        'qtd_maxima', 
        'permitir_repeticao',
        'permitir_exceder', 
        'preco_item_excedente',
        'limite_excedente'
    )
    search_fields = ('nome',)
    inlines = [ItemGrupoOpcaoInline]

    fields = (
        'nome', 
        'qtd_minima', 
        'qtd_maxima', 
        'permitir_repeticao',
        'permitir_exceder', 
        'preco_item_excedente', 
        'limite_excedente'
    )

    class Media:
        js = ('loja/js/toggle_excedentes.js',)
        css = {
            'all': ('loja/css/custom_admin.css',)
        }


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'categoria', 
        'preco_base', 
        'preco_camada_extra', 
        'eh_customizavel', 
        'eh_combo', 
        'ativo'
    )
    list_filter = ('categoria', 'eh_customizavel', 'eh_combo', 'ativo')
    list_editable = ('preco_base', 'preco_camada_extra', 'eh_customizavel', 'eh_combo', 'ativo')
    search_fields = ('nome', 'descricao')
    filter_horizontal = ('grupos_opcoes',)
    inlines = [ItemComboInline]


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_cliente', 'telefone_cliente', 'valor_total', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome_cliente', 'telefone_cliente', 'id')
    readonly_fields = ('criado_em',)
