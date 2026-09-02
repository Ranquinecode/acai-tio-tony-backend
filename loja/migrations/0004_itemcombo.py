from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0003_cloudinary_fields'), # Ou o nome da sua última migração que está na pasta
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCombo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1, verbose_name='Quantidade deste item no combo')),
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens_do_combo', to='loja.produto')),
                ('produto_conteudo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presente_em_combos', to='loja.produto', verbose_name='Produto incluso')),
            ],
            options={
                'verbose_name': 'Item do Combo',
                'verbose_name_plural': 'Itens do Combo',
            },
        ),
    ]
