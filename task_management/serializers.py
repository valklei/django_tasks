from rest_framework import serializers
from task_management.models import Task


# HW12. Задание 1: Эндпоинт для создания задачи
# Задача должна быть создана с полями
# title, description, status, и deadline.

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


# HW12.  Задание 2: Эндпоинты для получения списка задач
# и конкретной задачи по её ID

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


class TaskByIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"