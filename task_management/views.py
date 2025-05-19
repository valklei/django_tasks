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
from task_management.utils import set_jwt_cookies
from task_management.permissions.owner_permissions import IsOwnerOrReadOnly
from rest_framework.pagination import PageNumberPagination
import datetime
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from task_management.models import Task, SubTask, Category
from task_management.serializers import (
    TaskCreateSerializer,
    TaskListSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategorySerializer,
    RegisterSerializer,
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



class LogInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user:
            response = Response(status=status.HTTP_200_OK)

            set_jwt_cookies(response=response, user=user)

            return response

        else:
            return Response(
                data={"message": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogOutAPIView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response


class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response = Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

        set_jwt_cookies(response, user)

        return response


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