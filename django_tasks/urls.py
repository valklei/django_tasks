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
from django.urls import path, include
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from itertools import permutations
from task_management import views
from task_management.views import (
    TaskDetailUpdateDeleteView,
    task_statistic,
    TaskListCreateView,
    SubTasklistCreateView,
    SubTaskDetailUpdateDeleteView,
    CategoryViewSet,
    UserTasksListGenericView,
    UserSubTasksListGenericView,
    LogInAPIView,
    LogOutAPIView,
    RegisterUserAPIView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
    openapi.Info(
        title='Tasks API',
        default_version='v1',
        description='Tasks API with permissions',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(name='Alex Narizhnyi', email='test.email@gmail.com'),
        license=openapi.License(name='OUR LICENSE', url='https://example.com')
    ),
    public=False,
    permission_classes=[permissions.IsAdminUser],
)

router = DefaultRouter()

router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.home, name='home'),
    path('hello/', views.hello_world, name='hello_world'),
    path('second/', views.second_view, name='second_view'),
    path('tasks/', TaskListCreateView.as_view()),
    path('tasks/<int:task_id>/', TaskDetailUpdateDeleteView.as_view()),
    path('tasks/statistic/', task_statistic),
    path('tasks/<int:weekday>', TaskDetailUpdateDeleteView.as_view()),
    path('tasks-me/', UserTasksListGenericView.as_view()),
    path('subtasks/', SubTasklistCreateView.as_view()),
    path('subtasks-me/', UserTasksListGenericView.as_view()),
    path('subtasks/<int:pk>', UserSubTasksListGenericView.as_view()),
    path('', include(router.urls)),
    path('login/', LogInAPIView.as_view()),
    path('logout/', LogOutAPIView.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('auth-login/', TokenObtainPairView.as_view()),
    path('auth-refresh-token/', TokenRefreshView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]

