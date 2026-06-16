import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods

from chat.models import Mensaje, Conversacion
from .serializers import ChatEntradaSerializer, ChatRespuestaSerializer
from .services import detectar_emocion, generar_respuesta


@login_required
def chat_page(request):
    """Carga el chat con la conversación activa del usuario."""
    # Obtener conversación activa (la más reciente) o crear una nueva
    conversacion = Conversacion.objects.filter(
        usuario=request.user
    ).first()

    if not conversacion:
        conversacion = Conversacion.objects.create(
            usuario=request.user,
            titulo='Nueva conversación'
        )

    # Todas las conversaciones del usuario para el sidebar
    conversaciones = Conversacion.objects.filter(usuario=request.user)

    # Mensajes de la conversación activa
    mensajes = conversacion.mensajes.all()

    return render(request, 'chat.html', {
        'conversacion': conversacion,
        'conversaciones': conversaciones,
        'mensajes': mensajes,
    })


@login_required
def cambiar_conversacion(request, conv_id):
    """Carga una conversación específica."""
    conversacion = get_object_or_404(
        Conversacion, id=conv_id, usuario=request.user
    )
    conversaciones = Conversacion.objects.filter(usuario=request.user)
    mensajes = conversacion.mensajes.all()

    return render(request, 'chat.html', {
        'conversacion': conversacion,
        'conversaciones': conversaciones,
        'mensajes': mensajes,
    })


@login_required
@require_POST
def nueva_conversacion(request):
    """Crea una nueva conversación y la retorna como JSON."""
    conv = Conversacion.objects.create(
        usuario=request.user,
        titulo='Nueva conversación'
    )
    return JsonResponse({
        'id': conv.id,
        'titulo': conv.titulo,
    })


@login_required
@require_http_methods(['DELETE'])
def eliminar_conversacion(request, conv_id):
    """Elimina una conversación completa."""
    conv = get_object_or_404(Conversacion, id=conv_id, usuario=request.user)
    conv.delete()
    return JsonResponse({'ok': True})


@login_required
@require_http_methods(['DELETE'])
def eliminar_mensaje(request, msg_id):
    """Elimina un mensaje específico."""
    mensaje = get_object_or_404(
        Mensaje, id=msg_id, usuario=request.user
    )
    mensaje.delete()
    return JsonResponse({'ok': True})


class ChatEmocionalView(APIView):
    """Endpoint principal del chat — recibe texto y devuelve respuesta IA."""

    def post(self, request):
        serializer = ChatEntradaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        texto     = serializer.validated_data["texto"]
        historial = serializer.validated_data.get("historial", [])
        conv_id   = request.data.get("conversacion_id")

        # Obtener o crear conversación
        if conv_id:
            try:
                conversacion = Conversacion.objects.get(
                    id=conv_id, usuario=request.user
                )
            except Conversacion.DoesNotExist:
                conversacion = Conversacion.objects.create(
                    usuario=request.user,
                    titulo=texto[:60]
                )
        else:
            conversacion = Conversacion.objects.create(
                usuario=request.user,
                titulo=texto[:60]
            )

        # Actualizar título si es el primer mensaje
        if conversacion.mensajes.count() == 0:
            conversacion.titulo = texto[:60]
            conversacion.save()

        # Detectar emoción
        try:
            resultado_emocion = detectar_emocion(texto)
        except Exception as e:
            return Response(
                {"error": "Error al detectar emoción.", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Generar respuesta
        try:
            respuesta = generar_respuesta(
                texto=texto,
                emocion=resultado_emocion["emocion_es"],
                historial=historial
            )
        except Exception as e:
            return Response(
                {"error": "Error al generar respuesta.", "detalle": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Guardar mensaje
        mensaje = Mensaje.objects.create(
            conversacion=conversacion,
            usuario=request.user,
            texto=texto,
            emocion_detectada=resultado_emocion["emocion_es"],
            respuesta_ia=respuesta
        )

        datos_respuesta = {
            "mensaje_id":        mensaje.id,
            "texto":             mensaje.texto,
            "emocion_detectada": mensaje.emocion_detectada,
            "confianza_pct":     resultado_emocion["confianza_pct"],
            "respuesta_ia":      mensaje.respuesta_ia,
            "fecha_creacion":    mensaje.fecha_creacion,
            "conversacion_id":   conversacion.id,
            "conversacion_titulo": conversacion.titulo,
        }

        return Response(
            ChatRespuestaSerializer(datos_respuesta).data,
            status=status.HTTP_200_OK
        )