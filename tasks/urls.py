from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('<int:task_id>/update/', views.task_update, name='task_update'),
    path('<int:task_id>/delete/', views.task_delete, name='task_delete'),
    path('complete/<int:task_id>/', views.complete_task, name='task_complete'),
    path('daily/', views.daily_tasks, name='daily_tasks'),
    path('daily/complete/<int:task_id>/', views.complete_daily_task, name='complete_daily_task'),
    path('test-404/', views.test_404, name='test_404'),
]

