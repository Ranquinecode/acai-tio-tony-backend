from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Categoria,
    CategoriaItemAdicional,
    ItemAdicional, 
    GrupoOpcao, 
    ItemGrupoOpcao, 
    Produto, 
    ProdutoGrupoOpcao,
    Pedido,
    ItemCombo,
    ItemGrupoOpcaoFilho
)


# ==========================================
# INLINES (Formulários em Bloco)
# ==========================================

class ItemGrupoOpcaoInline(admin.TabularInline):
    model = ItemGrupoOpcao
    extra = 1
    autocomplete_fields = ['item']
    verbose_name = "Item deste Grupo"
    verbose_name_plural = "Itens e Ordem de Exibição neste Grupo"
    fields = ('ordem', 'item', 'preco_especifico')
    ordering = ('ordem',)


class ProdutoGrupoOpcaoInline(admin.TabularInline):
    model = ProdutoGrupoOpcao
    extra = 1
    autocomplete_fields = ['grupo_opcao']
    verbose_name = "Grupo de Opções do Produto"
    verbose_name_plural = "Grupos de Opções (Com Ordem de Exibição)"
    fields = ('ordem', 'grupo_opcao')
    ordering = ('ordem',)


class ItemComboInline(admin.TabularInline):
    model = ItemCombo
    fk_name = 'combo'
    extra = 1
    verbose_name = "Produto do Combo"
    verbose_name_plural = "Produtos que compõem este Combo"
    autocomplete_fields = ['produto_conteudo']
    fields = ('ordem', 'produto_conteudo', 'quantidade')
    classes = ('item-combo-inline-group',)


# ==========================================
# ADMIN REGISTRATIONS
# ==========================================

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem', 'ativo')
    list_editable = ('ordem', 'ativo')
    search_fields = ('nome',)
    ordering = ('ordem', 'nome')


@admin.register(CategoriaItemAdicional)
class CategoriaItemAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ordem')
    list_editable = ('ordem',)
    search_fields = ('nome',)
    ordering = ('ordem', 'nome')


@admin.register(ItemAdicional)
class ItemAdicionalAdmin(admin.ModelAdmin):
    list_display = ('preview_imagem', 'nome', 'categoria_item', 'disponibilidade')
    list_editable = ('categoria_item', 'disponibilidade')
    list_filter = ('disponibilidade', 'categoria_item')
    search_fields = ('nome',)
    ordering = ('categoria_item__ordem', 'nome')

    @admin.display(description='Foto')
    def preview_imagem(self, obj):
        if obj.imagem_url:
            return format_html(
                '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.imagem_url
            )
        return format_html('<span style="color: #999; font-size: 11px;">Sem Imagem</span>')


@admin.register(GrupoOpcao)
class GrupoOpcaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 
        'qtd_minima', 
        'qtd_maxima', 
        'permitir_repeticao',
        'cobrar_camada_extra',
        'permitir_exceder', 
        'preco_item_excedente',
        'limite_excedente'
    )
    list_editable = (
        'qtd_minima', 
        'qtd_maxima', 
        'permitir_repeticao',
        'cobrar_camada_extra',
        'permitir_exceder', 
        'preco_item_excedente',
        'limite_excedente'
    )
    search_fields = ('nome',)
    inlines = [ItemGrupoOpcaoInline]

    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome',)
        }),
        ('Regras de Escolha e Obrigatoriedade', {
            'fields': ('qtd_minima', 'qtd_maxima', 'permitir_repeticao', 'cobrar_camada_extra')
        }),
        ('Regras para Itens Excedentes (Extras Cobrados)', {
            'fields': ('permitir_exceder', 'preco_item_excedente', 'limite_excedente')
        }),
    )

    class Media:
        js = ('loja/js/admin_custom.js',)
        css = {
            'all': ('loja/css/admin_custom.css',)
        }


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'preview_imagem',
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
    inlines = [ProdutoGrupoOpcaoInline, ItemComboInline]

    fieldsets = (
        ('Informações Principais', {
            'fields': ('nome', 'categoria', 'descricao', 'imagem', 'ativo')
        }),
        ('Preços e Tipo de Produto', {
            'fields': ('preco_base', 'preco_camada_extra', 'eh_customizavel', 'eh_combo')
        }),
    )

    @admin.display(description='Foto')
    def preview_imagem(self, obj):
        if obj.imagem_url:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.imagem_url
            )
        return format_html('<span style="color: #999; font-size: 11px;">Sem Imagem</span>')

    class Media:
        js = ('loja/js/admin_custom.js',)
        css = {
            'all': ('loja/css/admin_custom.css',)
        }


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_cliente', 'telefone_cliente', 'valor_total', 'status', 'criado_em')
    list_filter = ('status', 'criado_em')
    search_fields = ('nome_cliente', 'telefone_cliente', 'id')
    readonly_fields = (
        'criado_em', 
        'nome_cliente', 
        'telefone_cliente', 
        'endereco_completo', 
        'payload_itens', 
        'valor_produtos', 
        'taxa_entrega', 
        'valor_total', 
        'mercado_pago_id'
    )

    fieldsets = (
        ('Status do Pedido', {
            'fields': ('status', 'criado_em')
        }),
        ('Informações do Cliente', {
            'fields': ('nome_cliente', 'telefone_cliente', 'endereco_completo')
        }),
        ('Detalhes da Compra e Pagamento', {
            'fields': ('payload_itens', 'valor_produtos', 'taxa_entrega', 'valor_total', 'mercado_pago_id')
        }),
    )
