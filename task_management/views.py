from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import ExtractWeekDay
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from task_management.models import Task, SubTask
from task_management.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)

def hello_world(request):
     return HttpResponse("<h1>hello world</h1>")

def second_view(request):
     return HttpResponse("<h1>Hello! It's my second view!</h1>")

def home(request):
     return render(request, 'home.html')


@api_view(['POST'])
def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=201)
    else:
        return Response(serializer.errors,status=404)


class SubTaskListCreateAPIView(APIView):

    def get(self, request: Request):
        queryset: QuerySet[SubTask] = SubTask.objects.all()
        serializer = SubTaskSerializer(queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


    def post(self, request: Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        try:
            subtask = SubTask.objects.get(id=kwargs['subtask_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found",
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = SubTaskSerializer(subtask)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, **kwargs) -> Response:
        try:
            subtask = SubTask.objects.get(id=kwargs['book_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = SubTaskSerializer(instance=subtask, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request: Request, **kwargs) -> Response:
        try:
            subtask = SubTask.objects.get(id=kwargs['book_id'])
        except SubTask.DoesNotExist:
            return Response(
                data={
                    "message": "Subtask not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        subtask.delete()

        return Response(
            data={
                "message": "Subtask was deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )
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