from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import FormularioRegistro, FormularioLogin


def vista_login(request):
    """Formulario de login"""
    if request.user.is_authenticated:
        return redirect('/chat/')

    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/chat/')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = FormularioLogin(request)

    return render(request, 'usuarios/login.html', {'form': form})


def vista_registro(request):
    """Formulario de registro"""
    if request.user.is_authenticated:
        return redirect('/chat/')

    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # login automático al registrarse
            messages.success(request, f'¡Bienvenido, {user.username}!')
            return redirect('/chat/')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = FormularioRegistro()

    return render(request, 'usuarios/registro.html', {'form': form})


def vista_logout(request):
    """Cierra sesión y redirige al login"""
    logout(request)
    return redirect('/login/')


def vista_recuperar(request):
    """Formulario de recuperación de contraseña"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=False,
                email_template_name='usuarios/email_recuperar.html',
                subject_template_name='usuarios/email_asunto.txt',
            )
            return render(request, 'usuarios/recuperar_enviado.html')
    else:
        form = PasswordResetForm()

    return render(request, 'usuarios/recuperar.html', {'form': form})