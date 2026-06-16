
from rest_framework import serializers


class MensajeHistorialSerializer(serializers.Serializer):
    """
    Serializer para cada mensaje dentro del historial de conversación.

    El historial es una lista de mensajes anteriores que el cliente
    guarda y envía en cada petición para que la IA recuerde el contexto.

    Estructura de cada mensaje del historial:
        {"role": "user",      "content": "Estoy triste"}
        {"role": "assistant", "content": "Ey, ¿qué pasó?"}
    """

    role = serializers.ChoiceField(
      
        choices=["user", "assistant"],
        error_messages={
            "invalid_choice": "El role debe ser 'user' o 'assistant'."
        }
    )

    content = serializers.CharField(
        
        max_length=5000,
        error_messages={
            "blank":      "El contenido del mensaje no puede estar vacío.",
            "max_length": "El mensaje no puede superar 5000 caracteres.",
        }
    )


class ChatEntradaSerializer(serializers.Serializer):
    """
    Valida el JSON que el cliente envía al endpoint del chat.

    Ejemplo de JSON de entrada con historial:
    {
        "texto": "Hoy me siento muy mal, todo salió mal",
        "historial": [
            {"role": "user",      "content": "Hola"},
            {"role": "assistant", "content": "¡Hola! ¿Cómo estás?"}
        ]
    }

    Ejemplo de JSON de entrada sin historial (primer mensaje):
    {
        "texto": "Hola, ¿cómo estás?"
    }
    """

    texto = serializers.CharField(
        min_length=2,
        max_length=5000,
        trim_whitespace=True,
        error_messages={
            "blank":      "El mensaje no puede estar vacío.",
            "min_length": "El mensaje debe tener al menos 2 caracteres.",
            "required":   "El campo 'texto' es obligatorio.",
        }
    )

    historial = MensajeHistorialSerializer(
       
        many=True,
        

        required=False,
        

        default=list
       
    )


class ChatRespuestaSerializer(serializers.Serializer):
    """
    Define la estructura del JSON que la API devuelve al cliente
    después de procesar un mensaje del chat emocional.

    Ejemplo de respuesta:
    {
        "mensaje_id":        3,
        "texto":             "Hoy me siento muy mal",
        "emocion_detectada": "tristeza",
        "confianza_pct":     "94.21%",
        "respuesta_ia":      "Uy parcero, ¿qué pasó? Cuéntame...",
        "fecha_creacion":    "2026-03-17T10:00:00-05:00"
    }
    """

    mensaje_id = serializers.IntegerField(read_only=True)
    texto = serializers.CharField(read_only=True)
    emocion_detectada = serializers.CharField(read_only=True)
    confianza_pct = serializers.CharField(read_only=True)
    respuesta_ia = serializers.CharField(read_only=True)
    fecha_creacion = serializers.DateTimeField(read_only=True)
    
