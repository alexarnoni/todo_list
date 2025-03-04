import os
import django
import random
from datetime import datetime, timedelta

# Configura o ambiente Django para acessar os modelos
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "todolist.settings")
django.setup()

from tasks.models import Task
from django.contrib.auth.models import User

# Função para criar usuários fictícios
def create_users():
    users = []
    for i in range(3):
        username = f"user{i+1}"
        user, created = User.objects.get_or_create(username=username, defaults={"password": "test1234"})
        users.append(user)
    print("Usuários criados ou recuperados:", users)  # Agora verifica se há usuários criados ou recuperados
    return users

# Função para criar tarefas fictícias
def create_tasks():
    users = create_users()
    task_titles = [
        "Finalizar relatório de vendas",
        "Revisar código do projeto",
        "Fazer compras do mercado",
        "Agendar consulta médica",
        "Responder emails pendentes",
        "Planejar viagem de férias",
        "Treinar para a maratona",
        "Estudar para a certificação",
        "Fazer backup dos arquivos",
        "Atualizar o portfólio"
    ]
    
    for _ in range(20):  # Criar 20 tarefas
        user = random.choice(users)
        title = random.choice(task_titles)
        description = f"Descrição de {title}"
        completed = random.choice([True, False])
       
        Task.objects.create(
            user=user,
            title=title,
            description=description,
            completed=completed,
        )

    print("✅ Banco de dados populado com tarefas fictícias!")

# Executa a criação de tarefas
if __name__ == "__main__":
    create_tasks()
