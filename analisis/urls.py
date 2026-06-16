from django.urls import path
from .views import (
    ChatEmocionalView,
    chat_page,
    nueva_conversacion,
    cambiar_conversacion,
    eliminar_conversacion,
    eliminar_mensaje,
)

urlpatterns = [
    path('chat/',                          ChatEmocionalView.as_view(), name='chat-api'),
    path('nueva-conversacion/',            nueva_conversacion,          name='nueva-conversacion'),
    path('conversacion/<int:conv_id>/',    cambiar_conversacion,        name='cambiar-conversacion'),
    path('conversacion/<int:conv_id>/eliminar/', eliminar_conversacion, name='eliminar-conversacion'),
    path('mensaje/<int:msg_id>/eliminar/', eliminar_mensaje,            name='eliminar-mensaje'),
]