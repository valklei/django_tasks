from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import ExtractWeekDay
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.request import Request
from rest_framework.views import APIView
from django.db.models import Count, QuerySet
from django.http import JsonResponse
from task_management.permissions.owner_permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
from task_management.models import Task, SubTask, Category
from task_management.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

def hello_world(request):
     return HttpResponse("<h1>hello world</h1>")

def second_view(request):
     return HttpResponse("<h1>Hello! It's my second view!</h1>")

def home(request):
     return render(request, 'home.html')



class UserSubTasksListGenericView(ListAPIView):
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        return SubTask.objects.filter(
            owner=self.request.user
        )


class SubTasklistCreateView(ListCreateAPIView):
    queryset: QuerySet[SubTask] = SubTask.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset: QuerySet[SubTask] = SubTask.objects.all()
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SubTaskSerializer
        return SubTaskCreateSerializer


class UserTasksListGenericView(ListAPIView):
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        return Task.objects.filter(
            owner=self.request.user
        )


class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields= ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskListSerializer
        return TaskCreateSerializer

    def perform_create(self, serializer):
        return serializer.seve(owner=self.request.user)


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [
        IsOwnerOrReadOnly
    ]

    lookup_url_kwarg = 'task_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskCreateSerializer



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly
    ]

    @action(
        detail=False,
        methods=['get', ],
        url_path='statistic'
    )
    def get_tasks_count_by_category(self, request: Request) -> Response:
        categories_statistic = Category.objects.annotate(
            count_tasks=Count('task')
        )

        data = [
            {
                "id": c.id,
                "name": c.name,
                "count_tasks": c.count_tasks,
            }
            for c in categories_statistic
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )


###############################################################
#
# class SubTaskListCreateAPIView(APIView, PageNumberPagination):
#     page_size = 5
#
#     def get_queryset(self, request: Request):
#
#         queryset: QuerySet[SubTask] = SubTask.objects.all()
#
#         # FILTER PARAMS
#         title = request.query_params.get('title')
#         status_sub = request.query_params.get('status')
#
#         # SORT PARAMS
#         sort_by = 'created_at'
#         sort_order = request.query_params.get('order', 'asc')
#
#         if title:
#             queryset = queryset.filter(
#                 task__title=title
#             )
#         if status_sub:
#             queryset = queryset.filter(
#                 status=status_sub
#             )
#
#         if sort_order == 'desc':
#             sort_by = f"-{sort_by}"
#
#             queryset = queryset.order_by(sort_by)
#
#         return queryset
#
#     def post(self, request: Request) -> Response:
#         serializer = SubTaskCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def get_page_size(self, request):
#         page_size = request.query_params.get('page_size')
#
#         if page_size and page_size.isdigit():
#             return int(page_size)
#
#         return self.page_size
#
#     def get(self, request: Request) -> Response:
#         subtasks = self.get_queryset(request=request)
#         results = self.paginate_queryset(queryset=subtasks, request=request, view=self)
#         serializer = SubTaskSerializer(results, many=True)
#
#         return self.get_paginated_response(data=serializer.data)
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#     def get(self, request: Request, **kwargs) -> Response:
#         try:
#             subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#         except SubTask.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Subtask not found",
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#         serializer = SubTaskSerializer(subtask)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def put(self, request: Request, **kwargs) -> Response:
#         try:
#             subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#         except SubTask.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Subtask not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = SubTaskSerializer(instance=subtask, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )
#
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def delete(self, request: Request, **kwargs) -> Response:
#         try:
#             subtask = SubTask.objects.get(id=kwargs['subtask_id'])
#         except SubTask.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Subtask not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         subtask.delete()
#
#         return Response(
#             data={
#                 "message": "Subtask was deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )
# # @api_view(['GET'])
# # def task_list(request):
# #     tasks = Task.objects.all()
# #     serializer = TaskListSerializer(tasks, many=True)
# #     return Response(serializer.data, status=200)
#
# from rest_framework.views import APIView
# from rest_framework.request import Request
# from django.db.models import QuerySet
# from .models import Task  # Убедитесь, что Task импортирован из правильного места
#
# class TaskListAPIView(APIView):
#     def get_queryset(self, request: Request) -> QuerySet[Task]:
#         queryset: QuerySet[Task] = Task.objects.all()
#
#         # FILTER PARAMS
#         weekday = request.query_params.get('weekday')
#         if weekday:
#             try:
#                 weekday = int(weekday)
#                 filtered_queryset = Task.objects.filter(created_at__week_day=weekday)
#                 if filtered_queryset.exists():
#                     queryset = filtered_queryset
#             except ValueError:
#                 pass  # Оставляем queryset без изменений при ошибке преобразования
#
#         return queryset
#
#     def get(self, request: Request) -> Response:
#         try:
#             queryset = self.get_queryset(request)
#             serializer = TaskListSerializer(queryset, many=True)
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )
#         except ValueError:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def post(self, request: Request):
#         serializer = TaskCreateSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#
# # @api_view(['GET'])
# # def task_list(request):
# #     tasks = Task.objects.all()
# #     serializer = TaskListSerializer(tasks, many=True)
# #     return Response(serializer.data, status=200)
#
# @api_view(['GET'])
# def task_detail(request, task_id):
#     try:
#         task = Task.objects.get(id=task_id)
#     except Task.DoesNotExist:
#         return Response(
#             {"message": "Task not found"},
#         )
#
#     serializer = TaskListSerializer(task)
#     return Response(serializer.data, status=200)
#
#
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