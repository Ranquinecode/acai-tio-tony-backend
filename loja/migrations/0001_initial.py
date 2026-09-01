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
                ('ordem', models.IntegerField(default=0)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemAdicional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco', models.DecimalField(decimal_places=2, default=0.0, max_digits=6)),
            ],
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
        ),
        migrations.CreateModel(
            name='GrupoOpcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('qtd_minima', models.IntegerField(default=0)),
                ('qtd_maxima', models.IntegerField(default=1)),
                ('itens', models.ManyToManyField(to='loja.itemadicional')),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco_base', models.DecimalField(decimal_places=2, max_digits=6)),
                ('preco_camada_extra', models.DecimalField(decimal_places=2, default=2.0, max_digits=6)),
                ('imagem_url', models.URLField(blank=True)),
                ('ativo', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loja.categoria')),
                ('grupos_opcoes', models.ManyToManyField(blank=True, to='loja.grupoopcao')),
            ],
        ),
    ]
