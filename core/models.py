from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=100, help_text="Nome completo do aluno")
    cpf = models.CharField(max_length=14, unique=True, help_text="CPF no formato 000.000.000-00")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    endereco = models.CharField(max_length=255, blank=True, verbose_name="Endereço Completo")
    data_inscricao = models.DateField(auto_now_add=True, verbose_name="Data de Inscrição")
    plano = models.ForeignKey('PlanoMensalidade', on_delete=models.SET_NULL, null=True, blank=True, related_name='alunos', verbose_name="Plano de Mensalidade")

    def __str__(self):
        return self.nome

class PlanoMensalidade(models.Model):
    """Modelo para tipos de mensalidade que podem ser editados pelo administrador"""
    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    
    class Meta:
        verbose_name = "Plano de Mensalidade"
        verbose_name_plural = "Planos de Mensalidade"
        ordering = ['valor']
    
    def __str__(self):
        return f"{self.descricao} - R$ {self.valor:.2f}"

class Mensalidade(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='mensalidades')
    plano = models.ForeignKey(PlanoMensalidade, on_delete=models.SET_NULL, null=True, blank=True, related_name='mensalidades')
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    paga = models.BooleanField(default=False)

    def __str__(self):
        status = "Paga" if self.paga else "Pendente"
        return f"Mensalidade de {self.aluno.nome} - Venc: {self.data_vencimento.strftime('%d/%m/%Y')} ({status})"