from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .form import TaskForm
from .models import tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required

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
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Contraseña no coinciden'
        })

@login_required
def task(request):
    task_show = tasks.objects.filter(
        user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': task_show
    })
@login_required
def task_complete(request):
    task_show = tasks.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': task_show
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
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Ingrese datos validos'
            })

@login_required
def task_detail(request, id):
    if request.method == 'GET':
        taks = get_object_or_404(tasks, pk=id, user=request.user)
        form = TaskForm(instance=taks)
        return render(request, 'task_detail.html', {
            'task': taks,
            'form': form
        })
    else:
        try:
            taks = get_object_or_404(tasks, pk=id, user=request.user)
            form = TaskForm(request.POST, instance=taks)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': taks,
                'form': form,
                'error':'Error al actualizar'
            })

@login_required
def complete_task(request, id):
    complete = get_object_or_404(tasks, pk=id, user=request.user)
    if request.method == 'POST':
        complete.datecompleted = timezone.now()
        complete.save()
        return redirect('tasks')

@login_required
def delete_task(request, id):
    complete = get_object_or_404(tasks, pk=id, user=request.user)
    if request.method == 'POST':
        complete.delete()
        return redirect('tasks')    

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
                'error': 'Usuario ó contraseña incorrécto'
            })
        else:
            login(request, user)
            return redirect('tasks')
