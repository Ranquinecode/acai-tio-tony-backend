from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0001_initial'),  # Se a sua migração inicial tiver outro nome, o Django ajusta automaticamente
    ]

    operations = [
        migrations.AddField(
            model_name='grupoopcao',
            name='limite_excedente',
            field=models.IntegerField(
                default=0, 
                help_text='Quantidade MÁXIMA de itens EXTRAS que o cliente pode adicionar além da qtd_maxima'
            ),
        ),
    ]
