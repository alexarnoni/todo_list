# 📝 To-Do List API 🚀

Este é um projeto de API REST para gerenciamento de tarefas, desenvolvido com **Django REST Framework**.

## 📌 Tecnologias Utilizadas
- 🐍 **Python** 3.12
- 🕸 **Django** 5.x
- 🔥 **Django REST Framework**
- 📄 **Swagger e Redoc** para documentação da API
- 🗃 **SQLite3** (padrão) ou PostgreSQL/MySQL (opcional)

## 📂 Instalação e Configuração

### 🔧 1. Clone o Repositório
```bash
git clone 
cd todo-list-api

🐍 2. Crie e Ative um Ambiente Virtual
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/Mac
source venv/bin/activate

📦 3. Instale as Dependências
pip install -r requirements.txt

🛠 4. Execute as Migrações do Banco de Dados
python manage.py migrate

🚀 5. Inicie o Servidor
python manage.py runserver

A API estará disponível em http://127.0.0.1:8000/.

Documentação da API

Após iniciar o servidor, acesse:
Swagger UI: http://127.0.0.1:8000/swagger/
Redoc: http://127.0.0.1:8000/redoc/

📮 Endpoints Principais
Método	Rota	Descrição
POST	/api/token/	Obter Token JWT
POST	/api/token/refresh/	Atualizar Token
GET	/api/tasks/	Listar todas as tarefas
POST	/api/tasks/	Criar uma nova tarefa
PUT	/api/tasks/{id}/	Atualizar uma tarefa
DELETE	/api/tasks/{id}/	Remover uma tarefa

🤝 Contribuição
Sinta-se à vontade para abrir issues ou enviar pull requests.

📜 Licença
Este projeto está sob a MIT License.