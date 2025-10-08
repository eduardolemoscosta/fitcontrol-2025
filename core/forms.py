from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'data_nascimento', 'email', 'telefone', 'endereco']
        # Você pode usar '__all__' para incluir todos os campos do modelo automaticamente
        # 