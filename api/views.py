from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .serializers import TodoSerializer, CompleteTodoSerializer
from todoapp.models import Todo
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User


class CurrentTodoList(ListCreateAPIView):
    model = Todo
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user, completed=None)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CompletedTodoList(ListAPIView):
    model = Todo
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user, completed__isnull=False)


class TodoDetail(RetrieveUpdateDestroyAPIView):
    model = Todo
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)


class TodoComplete(UpdateAPIView):
    serializer_class = CompleteTodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)

    def perform_update(self, serializer):
        serializer.instance.completed = timezone.now()
        serializer.save()


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': token.key}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'this user already exist'}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if not user:
            return JsonResponse({'error': 'Wrong username or password'}, status=400)
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return JsonResponse({'token': token.key}, status=200)
