
from django.db import migrations, models


class Migration(migrations.Migration):


    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='respuesta_ia',
            field=models.TextField(
               
                blank=True,
                null=True,
                verbose_name='Respuesta de la IA',
                help_text='Respuesta conversacional generada por la IA para este mensaje'
            ),
        ),
    ]
