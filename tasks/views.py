from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import RegistrosDiarios
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Avg
from django.utils import timezone
from datetime import timedelta
from .models import Tarea


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Registrar el nuevo usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })

@login_required
def tasks(request):

    tareas = Tarea.objects.filter(user=request.user).order_by('fecha')

    registros = RegistrosDiarios.objects.filter(
        user=request.user
    ).order_by('-created')

    hoy = timezone.now()

    # Ultimos 7 días
    inicio_semana = hoy - timedelta(days=7)

    promedio_semanal = RegistrosDiarios.objects.filter(
        user=request.user,
        created__gte=inicio_semana
    ).aggregate(promedio=Avg('stress_level'))['promedio']

    # Ultimos 30 días
    inicio_mes = hoy - timedelta(days=30)

    promedio_mensual = RegistrosDiarios.objects.filter(
        user=request.user,
        created__gte=inicio_mes
    ).aggregate(promedio=Avg('stress_level'))['promedio']


    # Evitar None
    if promedio_semanal is None:
        promedio_semanal = 0

    if promedio_mensual is None:
        promedio_mensual = 0


    return render(request, 'tasks.html', {
        'registro': registros,
        'promedio_semanal': promedio_semanal,
        'promedio_mensual': promedio_mensual,
        'tareas': tareas
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            nuevo = form.save(commit=False)
            nuevo.user = request.user
            nuevo.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor ingresa datos validos'
            })


@login_required
def registros_detalle(request, registro_id):
    if request.method == 'GET':
        registro = get_object_or_404(RegistrosDiarios, pk=registro_id, user=request.user)
        form = TaskForm(instance=registro)
        return render(request, 'registros_detalle.html', {'registro': registro, 'form': form})
    else:
        try:
            registro = get_object_or_404(RegistrosDiarios, pk=registro_id, user=request.user)
            form = TaskForm(request.POST, instance = registro)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_details.html',{'task':registro, 'form': form, 'error':"Error al actualizar el registro"})
        

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'El usuario o la contraseña es incorrecta'
            })
        else:
            login(request, user)
            return redirect('tasks')


@login_required
def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        fecha = request.POST['fecha']

        Tarea.objects.create(
            user=request.user,
            titulo=titulo,
            fecha=fecha
        )

    return redirect('tasks')

@login_required
def completar_tarea(request, tarea_id):

    tarea = get_object_or_404(Tarea, id=tarea_id, user=request.user)

    tarea.completada = not tarea.completada
    tarea.save()

    return redirect('tasks')

@login_required
def eliminar_tarea(request, tarea_id):

    tarea = get_object_or_404(Tarea, id=tarea_id, user=request.user)
    tarea.delete()

    return redirect('tasks')
        


