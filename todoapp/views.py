from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from .models import Todo
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .forms import TodoForm, RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


@login_required(login_url='login')
def current(request):
    return render(request, 'todoapp/current.html', {'todos': Todo.objects.filter(completed=None, author=request.user)})


@login_required(login_url='login')
def completed_todos(request):
    return render(request, 'todoapp/completed.html', {'todos': Todo.objects.filter(author=request.user).exclude(completed=None)})


class CreateTodo(LoginRequiredMixin, CreateView):
    login_url = '/login'
    form_class = TodoForm
    model = Todo
    template_name = 'todoapp/create.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super(CreateTodo, self).form_valid(form)


class Register(CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'todoapp/register.html'
    success_url = '/'

    def form_valid(self, form):
        valid = super(Register, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


def login_user(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('current')
            else:
                messages.error(request, 'wrong username or password')
    return render(request, 'todoapp/login.html', {'form': form})


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


class TodoDetail(LoginRequiredMixin, DetailView):
    login_url = '/login'
    context_object_name = 'todo'
    template_name = 'todoapp/todo_detail.html'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)


@login_required(login_url='login')
def complete_todo(request, pk):
    if Todo.objects.get(pk=pk).author != request.user:
        return redirect('current')
    todo = Todo.objects.get(pk=pk)
    todo.completed = timezone.now()
    todo.save()
    return redirect('todo_detail', pk=pk)


class UpdateTodo(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Todo
    form_class = TodoForm
    template_name = 'todoapp/update.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('todo_detail', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)


class DeleteTodo(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    success_url = '/'

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)
