from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from tasks.serializers import TaskSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib.auth.models import User
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from tasks.serializers import TaskSerializer, TaskListSerializer

### 🔹 LOGIN VIEW SEPARADO ###
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("task-list")  # Redireciona para a lista de tarefas
        else:
            messages.error(request, "Usuário ou senha incorretos.")

    return render(request, "tasks/login.html")  # Apenas renderiza o login

### 🔹 LOGOUT ###
def logout_view(request):
    logout(request)
    return redirect("login")  # Redireciona para login após logout

### 🔹 REGISTRO SEPARADO ###
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Conta criada com sucesso! Agora faça login.")
            return redirect("login")  # Redireciona para login
        else:
            messages.error(request, "Erro ao criar conta. Verifique os campos.")
    else:
        form = UserCreationForm()

    return render(request, "tasks/register.html", {"register_form": form})

### 🔹 CRUD DE TAREFAS ###
class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD de Tarefas.
    - **Listar tarefas** → `GET /api/tasks/`
    - **Criar tarefa** → `POST /api/tasks/`
    - **Atualizar tarefa** → `PUT /api/tasks/{id}/`
    - **Deletar tarefa** → `DELETE /api/tasks/{id}/`
    - **Filtrar tarefas por status** → `GET /api/tasks/?completed=true`
    - **Buscar tarefas por título ou descrição** → `GET /api/tasks/?search=trabalho`
    - **Ordenar por data de criação ou vencimento** → `GET /api/tasks/?ordering=-due_date`
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  # Agora exige JWT
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['completed']
    ordering_fields = ['created_at', 'due_date']
    search_fields = ['title', 'description']

    def get_queryset(self):
        """Retorna apenas as tarefas do usuário autenticado."""
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Associa a nova tarefa ao usuário autenticado."""
        serializer.save(user=self.request.user)

### 🔹 LISTA DE TAREFAS ###
@login_required(login_url="login")
def index(request):
    tasks = Task.objects.filter(user=request.user)
    
    # Contagem de tarefas
    total_tasks = tasks.count()
    pending_tasks = tasks.filter(completed=False).count()
    completed_tasks = tasks.filter(completed=True).count()

    return render(request, "tasks/index.html", {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks
    })

### 🔹 CRIAR TAREFA ###
@login_required(login_url="login")
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Tarefa criada com sucesso!", extra_tags="django-message")
        else:
            messages.error(request, "Erro ao criar tarefa.", extra_tags="django-message")
    return redirect("task-list")

### 🔹 EDITAR TAREFA ###
@login_required(login_url="login")
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.title = request.POST.get("title")
        task.description = request.POST.get("description", "")
        
        # Se o usuário clicou no botão "Marcar como Concluído"
        if "mark_complete" in request.POST:
            task.completed = not task.completed  # Alterna entre concluído/não concluído
        
        task.save()
    
    return redirect("task-list")

### 🔹 DELETAR TAREFA ###
@login_required(login_url="login")
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "Tarefa excluída com sucesso!", extra_tags="django-message")
    return redirect("task-list")

def get_serializer_class(self):
    """Usa um serializer diferente para listagem e detalhes"""
    if self.action == 'list':
        return TaskListSerializer
    return TaskSerializer
    