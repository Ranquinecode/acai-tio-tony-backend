from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        ordering = ['ordem', 'nome']

    def __str__(self):
        return self.nome


class ItemAdicional(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Item Adicional'
        verbose_name_plural = 'Itens Adicionais'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} (R$ {self.preco})" if self.preco > 0 else self.nome


class GrupoOpcao(models.Model):
    nome = models.CharField(max_length=100)
    qtd_minima = models.IntegerField(default=0)
    qtd_maxima = models.IntegerField(default=1)
    itens = models.ManyToManyField(ItemAdicional)

    class Meta:
        verbose_name = 'Grupo de Opções'
        verbose_name_plural = 'Grupos de Opções'

    def __str__(self):
        return f"{self.nome} (Min: {self.qtd_minima} / Máx: {self.qtd_maxima})"


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    preco_base = models.DecimalField(max_digits=6, decimal_places=2)
    preco_camada_extra = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)
    grupos_opcoes = models.ManyToManyField(GrupoOpcao, blank=True)
    imagem_url = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)

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

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome_cliente} ({self.status})"
