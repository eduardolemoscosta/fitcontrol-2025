from django.shortcuts import render, redirect
from .models import Aluno
from .forms import AlunoForm

def inicio(request):
    # Lógica para o painel inicial
    return render(request, 'inicio.html')

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
    return render(request, 'cadastrar_aluno.html', {'form': form})

def mensalidades(request):
    # No futuro, aqui você buscaria as mensalidades do banco de dados
    return render(request, 'mensalidades.html')

def relatorios(request):
    # No futuro, aqui você prepararia os dados para os gráficos
    return render(request, 'relatorios.html')

def configuracoes(request):
    # No futuro, aqui você carregaria e salvaria as configurações
    return render(request, 'configuracoes.html')