from django.db import models
from django.contrib.auth.models import User


class Conversacion(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversaciones'
    )
    titulo = models.CharField(max_length=200, default='Nueva conversación')
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_ultimo_mensaje = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha_ultimo_mensaje']
        db_table = 'chat_conversacion'

    def __str__(self):
        return f"{self.titulo} — {self.usuario.username}"


class Mensaje(models.Model):
    conversacion = models.ForeignKey(
        Conversacion,
        on_delete=models.CASCADE,
        related_name='mensajes',
        null=True,
        blank=True
    )
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='mensajes',
        null=True,
        blank=True
    )
    texto = models.TextField(verbose_name='Texto del mensaje')
    emocion_detectada = models.CharField(max_length=50, blank=True, null=True)
    respuesta_ia = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha_creacion']
        db_table = 'chat_mensaje'

    def __str__(self):
        return f"[{self.emocion_detectada}] {self.texto[:50]}"