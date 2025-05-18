"""
URL configuration for django_task project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from task_management import views
from task_management.views import (
    task_detail,
    task_statistic,
    TaskListAPIView,
    SubTaskListCreateAPIView,
    SubTaskDetailUpdateDeleteView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('hello/', views.hello_world, name='hello_world'),
    path('second/', views.second_view, name='second_view'),
    path('tasks/', TaskListAPIView.as_view()),
    path('tasks/<int:task_id>/', task_detail),
    path('tasks/statistic/', task_statistic),
    path('tasks/<int:weekday>', TaskListAPIView.as_view()),
    path('subtasks', SubTaskListCreateAPIView.as_view()),
    path('subtasks/', SubTaskListCreateAPIView.as_view()),
    path('subtasks/<int:subtask_id>', SubTaskDetailUpdateDeleteView.as_view()),
]

