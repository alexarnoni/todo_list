from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from tasks.views import index, task_create, task_update, task_delete, login_view, logout_view, register_view

# Configuração do Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="To-Do List API",
        default_version="v1",
        description="API para gerenciar tarefas de um usuário.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="seu-email@email.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Permite que qualquer pessoa veja a documentação
)

urlpatterns = [
    path("", login_view, name="login"),  # Página inicial agora será a de login
    path("index/", index, name="task-list"),  # Redirecionar para index.html em vez de task_list.html
    path("create/", task_create, name="task-create"),
    path("update/<int:task_id>/", task_update, name="task-update"),
    path("delete/<int:task_id>/", task_delete, name="task-delete"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'), 
   
   
    # Redireciona a página inicial para a lista de tarefas
    path("", lambda request: redirect("/tasks/"), name="index"),

    # URLs do Swagger
    re_path(r"^swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('admin/', admin.site.urls),  # Habilita o painel de administração do Django
    path("", include("tasks.urls")),  # Inclui as URLs do app 'tasks'

]

