from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from analisis.views import chat_page, cambiar_conversacion  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('api/', include('chat.urls')),
    path('api/analisis/', include('analisis.urls')),
    path('chat/', chat_page, name='chat'),
    path('chat/conversacion/<int:conv_id>/', cambiar_conversacion, name='cambiar-conversacion'),
    path('', lambda request: redirect('/login/'), name='inicio'),
]