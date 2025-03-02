from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from tasks.serializers import TaskSerializer
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from django.contrib.auth.models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("task-list")  # Agora redireciona corretamente para index.html

    return render(request, "tasks/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")  # Redireciona para a página de login após logout

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("new_username")
        password = request.POST.get("new_password")
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect("login")  # Após criar conta, volta para a tela de login

    return render(request, "tasks/login.html")

class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD de Tarefas.
    - **Listar tarefas** → `GET /api/tasks/`
    - **Criar tarefa** → `POST /api/tasks/`
    - **Atualizar tarefa** → `PUT /api/tasks/{id}/`
    - **Deletar tarefa** → `DELETE /api/tasks/{id}/`
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Retorna apenas as tarefas do usuário autenticado.
        """
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associa a nova tarefa ao usuário autenticado.
        """
        serializer.save(user=self.request.user)

# @login_required(login_url="login") # Redireciona usuários não autenticados
# def task_list(request):
#     tasks = Task.objects.filter()# Apenas tarefas do usuário logado
#     return render(request, "tasks/task_list.html", {"tasks": tasks})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redireciona para a página principal
        else:
            form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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

@login_required(login_url="login")
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Garante que a tarefa pertence ao usuário logado
            task.save()
            return redirect("task-list")
    return redirect("task-list")

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

@login_required(login_url="login")
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect("task-list")  # Apenas remove a tarefa sem deslogar o usuário