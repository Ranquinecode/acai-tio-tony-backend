from django.db import migrations
import cloudinary.models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0002_itemadicional_imagem_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemadicional',
            name='imagem_url',
        ),
        migrations.RemoveField(
            model_name='produto',
            name='imagem_url',
        ),
        migrations.AddField(
            model_name='itemadicional',
            name='imagem',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='imagem'),
        ),
        migrations.AddField(
            model_name='produto',
            name='imagem',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='imagem'),
        ),
    ]
