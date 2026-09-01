from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ordem = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class ItemAdicional(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

class GrupoOpcao(models.Model):
    nome = models.CharField(max_length=100)
    qtd_minima = models.IntegerField(default=0)
    qtd_maxima = models.IntegerField(default=1)
    itens = models.ManyToManyField(ItemAdicional)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco_base = models.DecimalField(max_digits=6, decimal_places=2)
    preco_camada_extra = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)
    grupos_opcoes = models.ManyToManyField(GrupoOpcao, blank=True)
    imagem_url = models.URLField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

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

    def __str__(self):
        return f"Pedido #{self.id} - {self.nome_cliente}"
