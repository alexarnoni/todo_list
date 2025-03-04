from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, index, task_create, task_update, task_delete
from .views import login_view, register_view, logout_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path("api/", include(router.urls)),  # Garante que a API está funcionando
    
    # Página principal com a lista de tarefas
    path("index/", index, name="task-list"),  # Página principal com as tarefas

    # Endpoints para gerenciar tarefas via frontend
    path("create/", task_create, name="task-create"),  # Criar nova tarefa
    path("update/<int:task_id>/", task_update, name="task-update"),  # Atualizar tarefa
    path("delete/<int:task_id>/", task_delete, name="task-delete"),  # Excluir tarefa
    
    # Autenticação
    path("login/", login_view, name="login"),  # Página de login
    path("register/", register_view, name="register"),  # Página de registro
    path("logout/", logout_view, name="logout"),  # Logout do usuário

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
