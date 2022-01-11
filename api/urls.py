from django.urls import path, include
from .views import *

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('current/', CurrentTodoList.as_view()),
    path('completed/', CompletedTodoList.as_view()),
    path('todo/<int:pk>/', TodoDetail.as_view()),
    path('todo/<int:pk>/complete/', TodoComplete.as_view()),
    path('signup/', signup),
    path('login/', login_user)
]
