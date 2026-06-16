
from django.apps import AppConfig

class AnalisisConfig(AppConfig):
    # Tipo de campo para llaves primarias automáticas
    default_auto_field = 'django.db.models.BigAutoField'

    
    name = 'analisis'

  
    verbose_name = 'Análisis Emocional'
