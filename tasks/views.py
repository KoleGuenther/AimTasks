from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        Task.objects.create(
            user=request.user,
            title=title,
            description=description
        )
        messages.success(request, "Task created successfully!")  # this is how to use the flash message
        return redirect('task_list')
    return render(request, 'tasks/task_create.html')

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.completed = 'completed' in request.POST
        task.save()
        messages.success(request, "Task updated successfully!")
        return redirect('task_list')
    return render(request, 'tasks/task_update.html', {'task': task})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted!")
        return redirect('task_list')
    return render(request, 'tasks/task_delete.html', {'task': task})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.save()
    messages.success(request, f'"{task.title}" marked as complete!')
    return redirect('task_list')