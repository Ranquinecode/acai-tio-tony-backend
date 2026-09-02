from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('ordem', models.IntegerField(default=0, help_text='Ordem de exibição no site (1 vem primeiro)')),
                ('ativo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['ordem', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='GrupoOpcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Ex: Escolha até 3 adicionais, Caldas, etc.', max_length=100)),
                ('qtd_minima', models.IntegerField(default=0, help_text='Mínimo de itens obrigatórios neste grupo')),
                ('qtd_maxima', models.IntegerField(default=1, help_text='Máximo de itens inclusos/permitidos no grupo')),
                ('permitir_exceder', models.BooleanField(default=False, help_text='Se marcado, permite ao cliente selecionar mais itens que a qtd_maxima cobrando valor extra')),
                ('preco_item_excedente', models.DecimalField(decimal_places=2, default=0.0, help_text='Preço cobrado por CADA item adicional que ultrapassar a qtd_maxima', max_digits=6)),
                ('limite_excedente', models.IntegerField(default=0, help_text='Quantidade MÁXIMA de itens EXTRAS que o cliente pode adicionar além da qtd_maxima')),
            ],
            options={
                'verbose_name': 'Grupo de Opções',
                'verbose_name_plural': 'Grupos de Opções',
            },
        ),
        migrations.CreateModel(
            name='ItemAdicional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Item Adicional',
                'verbose_name_plural': 'Itens Adicionais',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_cliente', models.CharField(max_length=100)),
                ('telefone_cliente', models.CharField(max_length=20)),
                ('endereco_completo', models.JSONField()),
                ('payload_itens', models.JSONField()),
                ('valor_produtos', models.DecimalField(decimal_places=2, max_digits=6)),
                ('taxa_entrega', models.DecimalField(decimal_places=2, max_digits=6)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('status', models.CharField(default='pendente', max_length=20)),
                ('mercado_pago_id', models.CharField(blank=True, max_length=100)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Pedido',
                'verbose_name_plural': 'Pedidos',
                'ordering': ['-criado_em'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, help_text='Descrição dos ingredientes para combos ou produtos fixos')),
                ('preco_base', models.DecimalField(decimal_places=2, max_digits=6)),
                ('preco_camada_extra', models.DecimalField(decimal_places=2, default=2.0, max_digits=6)),
                ('eh_customizavel', models.BooleanField(default=True, help_text='Desmarque para produtos/combos com receita fixa (não abre o modal step-by-step)')),
                ('eh_combo', models.BooleanField(default=False, help_text='Marque se for um combo promocional')),
                ('imagem_url', models.URLField(blank=True)),
                ('ativo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='loja.categoria')),
                ('grupos_opcoes', models.ManyToManyField(blank=True, to='loja.grupoopcao')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='ItemGrupoOpcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preco_especifico', models.DecimalField(decimal_places=2, default=0.0, help_text='Preço do item para este grupo especificamente (ex: Nutella no 330ml vs 770ml)', max_digits=6)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_relacionados', to='loja.grupoopcao')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.itemadicional')),
            ],
            options={
                'verbose_name': 'Item do Grupo',
                'verbose_name_plural': 'Itens dos Grupos',
                'unique_together': {('grupo', 'item')},
            },
        ),
    ]
