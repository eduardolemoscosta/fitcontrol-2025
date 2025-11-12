from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('alunos/', views.lista_alunos, name='lista_alunos'),
    path('alunos/cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('alunos/<int:aluno_id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:aluno_id>/excluir/', views.excluir_aluno, name='excluir_aluno'),
    path('mensalidades/', views.mensalidades, name='mensalidades'),
    path('mensalidades/planos/criar/', views.criar_plano, name='criar_plano'),
    path('mensalidades/planos/<int:plano_id>/editar/', views.editar_plano, name='editar_plano'),
    path('mensalidades/planos/<int:plano_id>/excluir/', views.excluir_plano, name='excluir_plano'),
    path('relatorios/', views.relatorios, name='relatorios'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
