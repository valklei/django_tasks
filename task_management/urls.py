from django.urls import path
from . import views


urlpatterns = [ path('', views.home, name='home'),
    path('hello/', views.hello_world, name='hello_world'),
    path('second/', views.second_view, name='second_view'),
]