from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
]
