from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskCreateSerializer, TaskListSerializer
from task_management.models import Task
from django.db.models import Count
from django.http import JsonResponse

def hello_world(request):
     return HttpResponse("<h1>hello world</h1>")

def second_view(request):
     return HttpResponse("<h1>Hello! It's my second view!</h1>")

def home(request):
     return render(request, 'home.html')


# Create your views here.
@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status=404)


@api_view(['GET'])
def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskListSerializer(tasks, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {"message": "Task not found"},
        )

    serializer = TaskListSerializer(task)
    return Response(serializer.data, status=200)


def task_statistic(request):
    count_task = Task.objects.aggregate(total_tasks=Count('id'))
    count_task_by_status = Task.objects.values('status').annotate(task_count=Count('id'))
    status_counts = {item['status']: item['task_count'] for item in count_task_by_status}
    pending_tasks = Task.objects.filter(status='pending').count()
    response_data = {
        'count_task': count_task['total_tasks'],
        'pending_tasks': pending_tasks,
        'count_task_by_status': status_counts
    }
    return JsonResponse(response_data)
# Create your views here.
