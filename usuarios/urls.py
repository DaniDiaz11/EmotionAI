from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import FormularioNuevaContrasena

urlpatterns = [
    path('login/',     views.vista_login,    name='login'),
    path('registro/',  views.vista_registro, name='registro'),
    path('logout/',    views.vista_logout,   name='logout'),
    path('recuperar/', views.vista_recuperar, name='recuperar'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             form_class=FormularioNuevaContrasena,
             success_url='/reset/done/'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]