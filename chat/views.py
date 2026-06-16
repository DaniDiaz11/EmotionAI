from rest_framework import viewsets
from .models import Mensaje
from .serializers import MensajeSerializer

class MensajeViewSet(viewsets.ModelViewSet):
  

    queryset = Mensaje.objects.all()
    # Mensaje.objects → Manager del modelo, interfaz con la BD
    # .all() → retorna todos los registros como QuerySet (lazy)
    # El orden viene definido por Meta.ordering en el modelo: más reciente primero

    serializer_class = MensajeSerializer
    # Indica a DRF qué serializer usar para:
    # 1. Convertir instancias del modelo a JSON (respuestas)
    # 2. Validar y convertir JSON a instancias del modelo (peticiones)
