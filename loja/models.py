from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição no site (1 vem primeiro)")
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordem', 'nome']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome


class ItemAdicional(models.Model):
    nome = models.CharField(max_length=100)
    imagem_url = models.URLField(
        blank=True, 
        help_text="URL da imagem no Cloudinary (opcional). Recomendado: foto quadrada (1:1)."
    )

    class Meta:
        verbose_name = 'Item Adicional'
        verbose_name_plural = 'Itens Adicionais'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class GrupoOpcao(models.Model):
    nome = models.CharField(max_length=100, help_text="Ex: Escolha até 3 adicionais, Caldas, etc.")
    qtd_minima = models.IntegerField(default=0, help_text="Mínimo de itens obrigatórios neste grupo")
    qtd_maxima = models.IntegerField(default=1, help_text="Máximo de itens inclusos/permitidos no grupo")
    permitir_exceder = models.BooleanField(
        default=False, 
        help_text="Se marcado, permite ao cliente selecionar mais itens que a qtd_maxima cobrando valor extra"
    )
    preco_item_excedente = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00, 
        help_text="Preço cobrado por CADA item adicional que ultrapassar a qtd_maxima"
    )
    limite_excedente = models.IntegerField(
        default=0,
        help_text="Quantidade MÁXIMA de itens EXTRAS que o cliente pode adicionar além da qtd_maxima (ex: 2 para permitir no máximo +2 extras)"
    )

    class Meta:
        verbose_name = 'Grupo de Opções'
        verbose_name_plural = 'Grupos de Opções'

    def __str__(self):
        return self.nome


class ItemGrupoOpcao(models.Model):
    grupo = models.ForeignKey(GrupoOpcao, on_delete=models.CASCADE, related_name='itens_relacionados')
    item = models.ForeignKey(ItemAdicional, on_delete=models.CASCADE)
    preco_especifico = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00, 
        help_text="Preço do item para este grupo especificamente (ex: Nutella no 330ml vs 770ml)"
    )

    class Meta:
        verbose_name = 'Item do Grupo'
        verbose_name_plural = 'Itens dos Grupos'
        unique_together = ('grupo', 'item')

    def __str__(self):
        return f"{self.item.nome} no {self.grupo.nome} - R$ {self.preco_especifico}"


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, help_text="Descrição dos ingredientes para combos ou produtos fixos")
    preco_base = models.DecimalField(max_digits=6, decimal_places=2)
    preco_camada_extra = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)
    eh_customizavel = models.BooleanField(
        default=True, 
        help_text="Desmarque para produtos/combos com receita fixa (não abre o modal step-by-step)"
    )
    eh_combo = models.BooleanField(default=False, help_text="Marque se for um combo promocional")
    grupos_opcoes = models.ManyToManyField(GrupoOpcao, blank=True)
    imagem_url = models.URLField(blank=True, help_text="URL da foto principal do produto no Cloudinary")
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_base}"


class Pedido(models.Model):
    nome_cliente = models.CharField(max_length=100)
    telefone_cliente = models.CharField(max_length=20)
    endereco_completo = models.JSONField()
    payload_itens = models.JSONField()
    valor_produtos = models.DecimalField(max_digits=6, decimal_places=2)
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2)
    valor_total = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20, default='pendente')
    mercado_pago_id = models.CharField(max_length=100, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome_cliente} ({self.status})"
