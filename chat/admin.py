from django.contrib import admin
from .models import Mensaje



@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
   
    # list_display: columnas visibles en la tabla del admin
    list_display = ['id', 'texto_corto', 'emocion_detectada', 'fecha_creacion']

    # list_filter: filtros laterales en el admin
    list_filter = ['emocion_detectada', 'fecha_creacion']

    # search_fields: habilita la barra de búsqueda en el admin
    search_fields = ['texto', 'emocion_detectada']

    # readonly_fields: campos que no se pueden editar desde el admin
    readonly_fields = ['fecha_creacion']

    # ordering: orden por defecto en el admin
    ordering = ['-fecha_creacion']

    def texto_corto(self, obj):
        
        return obj.texto[:60] + '...' if len(obj.texto) > 60 else obj.texto

    # Nombre de la columna en el admin para el método texto_corto
    texto_corto.short_description = 'Texto del mensaje'
