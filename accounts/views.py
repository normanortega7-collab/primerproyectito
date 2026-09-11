from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PrestacionForm, DevolucionForm
from django.contrib import messages

from .models import Libro, Prestacion, Genero, Devolucion


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    return render(request, 'accounts/home.html')


@login_required
def libros_view(request):
    libros = Libro.objects.all()

    return render(
        request,
        'accounts/libros.html',
        {'libros': libros}
    )


@login_required
def prestaciones_view(request):
    prestaciones = Prestacion.objects.all()

    return render(
        request,
        'accounts/prestaciones.html',
        {'prestaciones': prestaciones}
    )


@login_required
def generos_view(request):
    generos = Genero.objects.all()

    return render(
        request,
        'accounts/generos.html',
        {'generos': generos}
    )

@login_required
def crear_prestacion_view(request):
    if request.method == 'POST':
        form = PrestacionForm(request.POST)

        if form.is_valid():
            prestacion = form.save(commit=False)
            prestacion.pre_usuario = request.user
            libro = prestacion.pre_lib
            cantidad = prestacion.pre_cantidad

            if cantidad > libro.lib_cantidad:
                messages.error(
                    request,
                    f'Solo hay {libro.lib_cantidad} unidad(es) disponibles.'
                )

                return render(
                    request,
                    'accounts/crear_prestacion.html',
                    {'form': form}
                )

            prestacion.save()

            libro.lib_cantidad -= cantidad
            libro.save()

            messages.success(
                request,
                'Prestación registrada correctamente.'
            )

            return redirect('prestaciones')

    else:
        form = PrestacionForm()

    return render(
        request,
        'accounts/crear_prestacion.html',
        {'form': form}
    )

@login_required
def crear_devolucion_view(request):
    if request.method == 'POST':
        form = DevolucionForm(request.POST)

        if form.is_valid():
            devolucion = form.save(commit=False)

            prestacion = devolucion.dev_prestacion
            cantidad_devolver = devolucion.dev_cantidad

            cantidad_ya_devuelta = sum(
                d.dev_cantidad
                for d in prestacion.devoluciones.all()
            )

            cantidad_pendiente = (
                prestacion.pre_cantidad - cantidad_ya_devuelta
            )

            if cantidad_devolver > cantidad_pendiente:
                messages.error(
                    request,
                    f'Solo quedan {cantidad_pendiente} unidad(es) '
                    f'pendientes de devolver.'
                )

                return render(
                    request,
                    'accounts/crear_devolucion.html',
                    {'form': form}
                )

            devolucion.save()

            libro = prestacion.pre_lib

            libro.lib_cantidad += cantidad_devolver
            libro.save()

            messages.success(
                request,
                'Devolución registrada correctamente.'
            )

            return redirect('prestaciones')

    else:
        form = DevolucionForm()

    return render(
        request,
        'accounts/crear_devolucion.html',
        {'form': form}
    )    