from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('try-on/', views.try_on, name='try_on'),
    path('result/<str:job_id>/', views.result, name='result'),
]
