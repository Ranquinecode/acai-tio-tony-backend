from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='Nome')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('ordem', models.PositiveIntegerField(default=0, verbose_name='Ordem de Exibição')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['ordem', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=150, verbose_name='Nome do Produto')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('descricao', models.TextField(blank=True, verbose_name='Descrição')),
                ('preco', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Preço')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produtos/', verbose_name='Imagem')),
                ('ativo', models.BooleanField(default=True, verbose_name='Ativo')),
                ('e_combo', models.BooleanField(default=False, verbose_name='É um Combo/Promoção?')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produtos', to='loja.categoria')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.CreateModel(
            name='ItemCombo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1, verbose_name='Quantidade deste item no combo')),
                ('ordem', models.PositiveIntegerField(default=0, verbose_name='Ordem de exibição')),
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_do_combo', to='loja.produto')),
                ('produto_conteudo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presente_em_combos', to='loja.produto', verbose_name='Produto incluso')),
            ],
            options={
                'verbose_name': 'Item do Combo',
                'verbose_name_plural': 'Itens do Combo',
            },
        ),
    ]
