from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer

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