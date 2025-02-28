from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskViewSet, index, task_create, task_update, task_delete, task_list
from .views import task_list, login_view, register_view, logout_view

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    # API REST (caso queira ativar depois)
    # path('', include(router.urls)), 
    path("", task_list, name="task-list"),  # Garante que a URL 'task-list' existe
    
    # Página principal com a lista de tarefas
    path("index/", index, name="task-list"),

    # Endpoints para gerenciar tarefas via frontend
    path("create/", task_create, name="task-create"),  # Certifique-se de que o nome corresponde ao template!
    path("update/<int:task_id>/", task_update, name="task-update"),
    path("delete/<int:task_id>/", task_delete, name="task-delete"),
    path("logout/", logout_view, name="logout"),

    path("", login_view, name="login"),  # Página inicial agora é a tela de login
    path("tasks/", task_list, name="task-list"),  # Lista de tarefas após login
    path("register/", register_view, name="register"),  # Cadastro de usuários
]
  