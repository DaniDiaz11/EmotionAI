from groq import Groq
from django.conf import settings

EMOCIONES_VALIDAS = ["alegría", "tristeza", "enojo", "miedo", "asco", "sorpresa", "neutral", "ansiedad", "calma"]

def _get_cliente():
    return Groq(api_key=settings.GROQ_API_KEY)


def detectar_emocion(texto: str) -> dict:
    
    if not texto or not texto.strip():
        raise ValueError("El texto no puede estar vacío.")

    cliente = _get_cliente()

    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Eres un detector de emociones. Analiza el texto del usuario y responde ÚNICAMENTE con un JSON válido, sin explicaciones, sin markdown, sin texto adicional.

El JSON debe tener exactamente este formato:
{"emocion": "<emocion>", "confianza": <numero>}

Emociones permitidas (elige solo una): alegría, tristeza, enojo, miedo, asco, sorpresa, neutral, ansiedad, calma

La confianza es un número entre 0.0 y 1.0 que indica qué tan seguro estás.
Ejemplo: {"emocion": "tristeza", "confianza": 0.92}"""
            },
            {
                "role": "user",
                "content": texto
            }
        ],
        max_tokens=50,
        temperature=0.1,  
    )

    raw = respuesta.choices[0].message.content.strip()

    # Parsear el JSON de respuesta
    import json
    try:
        datos = json.loads(raw)
        emocion = datos.get("emocion", "neutral").lower()
        confianza = float(datos.get("confianza", 0.85))

        # Validar que la emoción sea una de las permitidas
        if emocion not in EMOCIONES_VALIDAS:
            emocion = "neutral"
            confianza = 0.5

    except (json.JSONDecodeError, ValueError):
        emocion = "neutral"
        confianza = 0.5

    return {
        "emocion_en":    emocion,       
        "emocion_es":    emocion,
        "confianza":     round(confianza, 4),
        "confianza_pct": f"{confianza * 100:.1f}%",
    }



def generar_respuesta(texto: str, emocion: str, historial: list) -> str:
   
    cliente = _get_cliente()

    system_prompt = f"""Eres EmotionAI, un asistente especializado en bienestar emocional y salud mental.
    Tu objetivo es acompañar a las personas a comprender y gestionar sus emociones de manera saludable.

    El usuario siente: {emocion}.

    Cómo debes responder:
    - Saluda la emoción del usuario con empatía y sin juzgar
    - Ofrece una perspectiva reflexiva que ayude a entender mejor lo que siente
    - Da un consejo práctico y concreto relacionado con la emoción detectada
    - Usa un tono cálido pero profesional, como un psicólogo de confianza
    - Máximo 4 oraciones por respuesta — claro y directo
    - Nunca uses frases vacías como "Entiendo perfectamente cómo te sientes"
    - Si la situación parece seria, recomienda hablar con un profesional de salud mental
    - Habla siempre en español"""

    mensajes = [{"role": "system", "content": system_prompt}]
    mensajes.extend(historial[-10:])
    mensajes.append({"role": "user", "content": texto})

    respuesta = cliente.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=mensajes,
        max_tokens=200,
        temperature=0.85,
    )

    return respuesta.choices[0].message.content.strip()