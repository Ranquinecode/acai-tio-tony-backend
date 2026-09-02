from django.db import models
from cloudinary.models import CloudinaryField


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
    STATUS_DISPONIBILIDADE = (
        ('disponivel', 'Disponível'),
        ('esgotado', 'Esgotado (Exibe acinzentado/sem estoque)'),
        ('oculto', 'Oculto (Esconde totalmente do cliente)'),
    )

    nome = models.CharField(max_length=100)
    imagem = CloudinaryField(
        'imagem', 
        blank=True, 
        null=True, 
        help_text="Faça upload da imagem diretamente para o Cloudinary ou selecione da sua mídia."
    )
    disponibilidade = models.CharField(
        max_length=20,
        choices=STATUS_DISPONIBILIDADE,
        default='disponivel',
        help_text="Controla se o item aparece disponível, acinzentado (sem estoque) ou oculto para o cliente."
    )

    class Meta:
        verbose_name = 'Item Adicional / Opção'
        verbose_name_plural = 'Itens Adicionais / Opções'
        ordering = ['nome']

    @property
    def imagem_url(self):
        if self.imagem:
            return self.imagem.url
        return ""

    def __str__(self):
        status_txt = f" [{self.get_disponibilidade_display()}]" if self.disponibilidade != 'disponivel' else ""
        return f"{self.nome}{status_txt}"


class GrupoOpcao(models.Model):
    nome = models.CharField(max_length=100, help_text="Ex: Escolha a Base, Onde ficam os complementos?, Adicionais Grátis, etc.")
    
    # Regras de Escolha e Obrigatoriedade
    qtd_minima = models.IntegerField(
        default=0, 
        help_text="0 = Opcional (ex: Descartáveis). 1 ou + = Obrigatório (ex: Escolha a Base)"
    )
    qtd_maxima = models.IntegerField(
        default=1, 
        help_text="Máximo de escolhas inclusas no preço ou permitidas no grupo"
    )
    permitir_repeticao = models.BooleanField(
        default=True,
        help_text="Se marcado, permite escolher 2x ou mais do MESMO item (ex: 2x Bombom). Se desmarcado, cada item só pode 1x."
    )

    # Regras de Excedentes
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
        help_text="Quantidade MÁXIMA de itens EXTRAS que o cliente pode adicionar além da qtd_maxima"
    )

    # Regra para Cobrança por Camada/Local (Em cima, No meio, No fundo)
    cobrar_camada_extra = models.BooleanField(
        default=False,
        help_text="Se marcado, 1ª seleção é grátis e da 2ª em diante cobra o valor de preco_camada_extra configurado no produto."
    )

    class Meta:
        verbose_name = 'Grupo de Opções'
        verbose_name_plural = 'Grupos de Opções'

    def __str__(self):
        obrigatorio = "Obrigatório" if self.qtd_minima > 0 else "Opcional"
        return f"{self.nome} ({obrigatorio} - Mín: {self.qtd_minima} | Máx: {self.qtd_maxima})"


class ItemGrupoOpcao(models.Model):
    grupo = models.ForeignKey(GrupoOpcao, on_delete=models.CASCADE, related_name='itens_relacionados')
    item = models.ForeignKey(ItemAdicional, on_delete=models.CASCADE)
    preco_especifico = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00, 
        help_text="Preço do item para este grupo especificamente (ex: Nutella no 330ml vs 770ml)"
    )
    ordem = models.PositiveIntegerField(
        default=1,
        help_text="Define a ordem de exibição deste item DENTRO deste grupo (1 vem primeiro)"
    )
    
    # Subgrupos condicionais com suporte a ordem
    grupos_filhos = models.ManyToManyField(
        GrupoOpcao, 
        blank=True, 
        related_name='itens_pai',
        through='ItemGrupoOpcaoFilho',
        help_text="Subgrupos que abrem automaticamente quando esta opção é selecionada (ex: Selecionar 'Sorvete' abre 'Sabores de Sorvete')."
    )

    class Meta:
        verbose_name = 'Item do Grupo'
        verbose_name_plural = 'Itens dos Grupos'
        ordering = ['ordem', 'id']
        unique_together = ('grupo', 'item')

    def __str__(self):
        nome_item = self.item.nome if hasattr(self, 'item') and self.item else "Item desvinculado"
        nome_grupo = self.grupo.nome if hasattr(self, 'grupo') and self.grupo else "Grupo desvinculado"
        return f"{self.ordem}º - {nome_item} no {nome_grupo} (R$ {self.preco_especifico})"


class ItemGrupoOpcaoFilho(models.Model):
    item_grupo = models.ForeignKey(ItemGrupoOpcao, on_delete=models.CASCADE)
    grupo_filho = models.ForeignKey(GrupoOpcao, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(
        default=1,
        help_text="Ordem em que este subgrupo aparece quando a opção pai é selecionada"
    )

    class Meta:
        verbose_name = 'Subgrupo Condicional'
        verbose_name_plural = 'Subgrupos Condicionais'
        ordering = ['ordem']


class Produto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, help_text="Descrição dos ingredientes para combos ou produtos fixos")
    preco_base = models.DecimalField(max_digits=6, decimal_places=2)
    preco_camada_extra = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=2.00,
        help_text="Valor cobrado por cada camada extra selecionada em grupos com 'cobrar_camada_extra' ativo."
    )
    eh_customizavel = models.BooleanField(
        default=True, 
        help_text="Desmarque para produtos/combos com receita fixa (não abre o modal step-by-step)"
    )
    eh_combo = models.BooleanField(default=False, help_text="Marque se for um combo promocional")
    
    # Relação com Ordenação dos Grupos de Opções por Produto
    grupos_opcoes = models.ManyToManyField(
        GrupoOpcao, 
        through='ProdutoGrupoOpcao',
        blank=True,
        help_text="Grupos de opções PRINCIPAIS que aparecem no produto, com ordem definida."
    )
    
    imagem = CloudinaryField(
        'imagem', 
        blank=True, 
        null=True, 
        help_text="Faça upload da imagem principal do produto no Cloudinary."
    )
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    @property
    def imagem_url(self):
        if self.imagem:
            return self.imagem.url
        return ""

    def __str__(self):
        return f"{self.nome} - R$ {self.preco_base}"


class ProdutoGrupoOpcao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    grupo_opcao = models.ForeignKey(GrupoOpcao, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(
        default=1,
        help_text="Ordem exata de exibição deste grupo para ESTE produto (1 = Primeiro do topo)"
    )

    class Meta:
        verbose_name = 'Grupo de Opção do Produto'
        verbose_name_plural = 'Grupos de Opções do Produto'
        ordering = ['ordem']
        unique_together = ('produto', 'grupo_opcao')

    def __str__(self):
        return f"{self.ordem}º Grupo: {self.grupo_opcao.nome} no {self.produto.nome}"


class ItemCombo(models.Model):
    combo = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE, 
        related_name='itens_combo',
        help_text="O produto principal marcado como eh_combo=True"
    )
    produto_conteudo = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE, 
        related_name='presente_em_combos',
        verbose_name="Produto Incluído",
        help_text="Selecione um produto existente (ex: Copo 330ml) que fará parte deste combo."
    )
    quantidade = models.PositiveIntegerField(
        default=1, 
        help_text="Quantas unidades deste produto vêm no combo (ex: 2 para 2 copos de 330ml)"
    )
    ordem = models.PositiveIntegerField(
        default=1, 
        help_text="Ordem de personalização no frontend (1 = Copo 1, 2 = Copo 2, etc.)"
    )

    class Meta:
        verbose_name = 'Item do Combo'
        verbose_name_plural = 'Itens do Combo'
        ordering = ['ordem']

    def __str__(self):
        nome_conteudo = self.produto_conteudo.nome if hasattr(self, 'produto_conteudo') and self.produto_conteudo else "Produto desvinculado"
        nome_combo = self.combo.nome if hasattr(self, 'combo') and self.combo else "Combo desvinculado"
        return f"{self.quantidade}x {nome_conteudo} no combo {nome_combo}"


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
