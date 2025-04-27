from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from django.utils import timezone
from datetime import date

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        is_daily = request.POST.get('is_daily') == 'on'
        Task.objects.create(
            user=request.user,
            title=title,
            description=description,
            is_daily=is_daily,
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
        task.is_daily = request.POST.get('is_daily') == 'on'
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
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, f'"{task.title}" marked as complete!')
    return redirect('task_list')

@login_required
def complete_daily_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = True
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, f'"{task.title}" marked as complete!')
    return redirect('daily_tasks')

def daily_tasks(request):
    today = timezone.now().date()
    tasks = Task.objects.filter(user=request.user, is_daily=True)

    # count completed tasks
    completed_count = 0
    for task in tasks:
        task.done_today = (
            task.completed_at and task.completed_at.date() == today
        )
        if task.done_today:
            completed_count += 1

    # total daily tasks
    total_tasks = tasks.count()

    # calculate progress
    progress_percent = int((completed_count / total_tasks) * 100) if total_tasks > 0 else 0
    
    context = {
        'tasks': tasks,
        'completed_count': completed_count,
        'total_tasks': total_tasks,
        'progress_percent': progress_percent,
    }

    return render(request, 'tasks/daily_tasks.html', context)

# testing the 404 page
def test_404(request):
    raise Http404
