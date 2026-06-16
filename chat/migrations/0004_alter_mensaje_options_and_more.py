

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_mensaje_options_mensaje_usuario_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mensaje',
            options={'ordering': ['fecha_creacion']},
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='emocion_detectada',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='respuesta_ia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='texto',
            field=models.TextField(verbose_name='Texto del mensaje'),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='Nueva conversación', max_length=200)),
                ('fecha_inicio', models.DateTimeField(auto_now_add=True)),
                ('fecha_ultimo_mensaje', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'chat_conversacion',
                'ordering': ['-fecha_ultimo_mensaje'],
            },
        ),
        migrations.AddField(
            model_name='mensaje',
            name='conversacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to='chat.conversacion'),
        ),
    ]
