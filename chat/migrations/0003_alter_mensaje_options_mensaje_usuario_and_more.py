

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_mensaje_respuesta_ia'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mensaje',
            options={'ordering': ['fecha_creacion'], 'verbose_name': 'Mensaje', 'verbose_name_plural': 'Mensajes'},
        ),
        migrations.AddField(
            model_name='mensaje',
            name='usuario',
            field=models.ForeignKey(blank=True, help_text='Usuario dueño de este mensaje', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='emocion_detectada',
            field=models.CharField(blank=True, help_text='Emoción identificada por el modelo de IA', max_length=50, null=True, verbose_name='Emoción detectada'),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='respuesta_ia',
            field=models.TextField(blank=True, help_text='Respuesta empática y conversacional generada por Groq', null=True, verbose_name='Respuesta de la IA'),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='texto',
            field=models.TextField(help_text='Mensaje escrito por el usuario', verbose_name='Texto del mensaje'),
        ),
        migrations.AlterModelTable(
            name='mensaje',
            table='chat_mensaje',
        ),
    ]
