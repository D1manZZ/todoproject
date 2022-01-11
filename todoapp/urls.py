from django.urls import path
from .views import *

urlpatterns = [
    path('', current, name='current'),
    path('create/', CreateTodo.as_view(), name='create'),
    path('register/', Register.as_view(), name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('todo/<int:pk>/', TodoDetail.as_view(), name='todo_detail'),
    path('todo/<int:pk>/complete/', complete_todo, name='complete_todo'),
    path('todo/<int:pk>/edit/', UpdateTodo.as_view(), name='edit_todo'),
    path('todo/<int:pk>/delete/', DeleteTodo.as_view(), name='delete_todo'),
    path('completed/', completed_todos, name='completed')
]
