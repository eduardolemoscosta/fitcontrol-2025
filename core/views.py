from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from .models import Aluno, Mensalidade, PlanoMensalidade
from .forms import AlunoForm, PlanoMensalidadeForm

def inicio(request):
    # Contar alunos ativos (todos os alunos cadastrados)
    alunos_ativos = Aluno.objects.count()
    
    # Contar mensalidades pendentes (não pagas)
    mensalidades_pendentes = Mensalidade.objects.filter(paga=False).count()
    
    # Contar mensalidades vencidas (não pagas e com data de vencimento passada)
    hoje = date.today()
    mensalidades_vencidas = Mensalidade.objects.filter(paga=False, data_vencimento__lt=hoje).count()
    
    contexto = {
        'alunos_ativos': alunos_ativos,
        'mensalidades_pendentes': mensalidades_pendentes,
        'mensalidades_vencidas': mensalidades_vencidas,
    }
    return render(request, 'inicio.html', contexto)

def lista_alunos(request):
    alunos = Aluno.objects.all().order_by('nome') # Busca todos os alunos no banco
    contexto = {'alunos': alunos} # Cria um dicionário para enviar para o template
    return render(request, 'lista_alunos.html', contexto)

def cadastrar_aluno(request):
    if request.method == 'POST':
        # 2. Cria uma instância do formulário com os dados enviados (request.POST)
        form = AlunoForm(request.POST)
        
        # 3. O Django verifica se todos os dados são válidos
        if form.is_valid():
            form.save()  # 4. Salva o novo aluno no banco de dados
            return redirect('lista_alunos') # Redireciona para a lista
    else:
        # 5. Se for um GET, cria um formulário em branco
        form = AlunoForm()
        
    # 6. Envia o formulário (preenchido ou vazio) para o template
    return render(request, 'cadastrar_aluno.html', {'form': form, 'titulo': 'Cadastrar Aluno'})

def editar_aluno(request, aluno_id):
    """View para editar um aluno existente"""
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        form = AlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('lista_alunos')
    else:
        form = AlunoForm(instance=aluno)
    return render(request, 'cadastrar_aluno.html', {'form': form, 'aluno': aluno, 'titulo': 'Editar Aluno'})

def excluir_aluno(request, aluno_id):
    """View para excluir um aluno"""
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    if request.method == 'POST':
        aluno.delete()
        return redirect('lista_alunos')
    
    # Contar mensalidades associadas ao aluno
    quantidade_mensalidades = aluno.mensalidades.count()
    
    contexto = {
        'aluno': aluno,
        'quantidade_mensalidades': quantidade_mensalidades,
    }
    return render(request, 'confirmar_exclusao_aluno.html', contexto)

def mensalidades(request):
    # Buscar todos os planos de mensalidade ativos
    planos = PlanoMensalidade.objects.filter(ativo=True).order_by('valor')
    contexto = {
        'planos': planos,
    }
    return render(request, 'mensalidades.html', contexto)

def gerenciar_planos(request):
    """View para gerenciar (listar, criar, editar, excluir) planos de mensalidade"""
    planos = PlanoMensalidade.objects.all().order_by('valor')
    contexto = {
        'planos': planos,
    }
    return render(request, 'gerenciar_planos.html', contexto)

def criar_plano(request):
    """View para criar um novo plano de mensalidade"""
    if request.method == 'POST':
        form = PlanoMensalidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mensalidades')
    else:
        form = PlanoMensalidadeForm()
    return render(request, 'form_plano.html', {'form': form, 'titulo': 'Criar Plano de Mensalidade'})

def editar_plano(request, plano_id):
    """View para editar um plano de mensalidade existente"""
    plano = get_object_or_404(PlanoMensalidade, pk=plano_id)
    if request.method == 'POST':
        form = PlanoMensalidadeForm(request.POST, instance=plano)
        if form.is_valid():
            form.save()
            return redirect('mensalidades')
    else:
        form = PlanoMensalidadeForm(instance=plano)
    return render(request, 'form_plano.html', {'form': form, 'plano': plano, 'titulo': 'Editar Plano de Mensalidade'})

def excluir_plano(request, plano_id):
    """View para excluir um plano de mensalidade"""
    plano = get_object_or_404(PlanoMensalidade, pk=plano_id)
    if request.method == 'POST':
        plano.delete()
        return redirect('mensalidades')
    return render(request, 'confirmar_exclusao_plano.html', {'plano': plano})

def relatorios(request):
    # No futuro, aqui você prepararia os dados para os gráficos
    return render(request, 'relatorios.html')

def configuracoes(request):
    # No futuro, aqui você carregaria e salvaria as configurações
    return render(request, 'configuracoes.html')