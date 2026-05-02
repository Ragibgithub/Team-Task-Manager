from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create-task/', views.create_task, name='create_task'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
]

