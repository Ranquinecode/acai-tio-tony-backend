from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemadicional',
            name='imagem_url',
            field=models.URLField(
                blank=True, 
                help_text='URL da imagem no Cloudinary (opcional). Recomendado: foto quadrada (1:1).'
            ),
        ),
    ]
