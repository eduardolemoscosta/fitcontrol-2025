from django import forms
from django.db.models import Q
from .models import Aluno, PlanoMensalidade

class PlanoSelectWidget(forms.Select):
    """Widget customizado para mostrar planos inativos no select"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.planos_cache = {}
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            # Buscar plano no cache ou no banco
            if value not in self.planos_cache:
                try:
                    plano = PlanoMensalidade.objects.get(pk=value)
                    self.planos_cache[value] = plano
                except PlanoMensalidade.DoesNotExist:
                    self.planos_cache[value] = None
            
            plano = self.planos_cache.get(value)
            if plano and not plano.ativo:
                option['label'] = f"{label} (Inativo)"
                if 'attrs' not in option:
                    option['attrs'] = {}
                option['attrs']['style'] = 'color: #D69E2E;'
        return option

class AlunoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar planos ativos e o plano atual do aluno (se existir e estiver inativo)
        try:
            # Buscar planos ativos
            planos_ativos = PlanoMensalidade.objects.filter(ativo=True)
            
            # Se estiver editando um aluno existente e ele tiver um plano (mesmo que inativo), incluir esse plano
            # self.instance existe após super().__init__()
            if self.instance and self.instance.pk and self.instance.plano:
                plano_atual = self.instance.plano
                # Usar Q objects para incluir o plano atual mesmo que esteja inativo
                queryset = PlanoMensalidade.objects.filter(
                    Q(ativo=True) | Q(pk=plano_atual.pk)
                ).distinct().order_by('valor')
            else:
                queryset = planos_ativos.order_by('valor')
            
            self.fields['plano'].queryset = queryset
        except Exception:
            # Se houver erro (por exemplo, se a tabela não existir ainda), usar todos os planos
            self.fields['plano'].queryset = PlanoMensalidade.objects.all().order_by('valor')
        
        self.fields['plano'].empty_label = "Selecione um plano (opcional)"
        self.fields['plano'].required = False
        
        # Usar widget customizado para mostrar planos inativos
        self.fields['plano'].widget = PlanoSelectWidget(attrs={'class': 'form-control'})
    
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'data_nascimento', 'email', 'telefone', 'endereco', 'plano']
        labels = {
            'nome': 'Nome Completo',
            'cpf': 'CPF',
            'data_nascimento': 'Data de Nascimento',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
            'plano': 'Plano de Mensalidade',
        }

class PlanoMensalidadeForm(forms.ModelForm):
    class Meta:
        model = PlanoMensalidade
        fields = ['descricao', 'valor', 'ativo']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Ex: Plano Básico'}),
            'valor': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor (R$)',
            'ativo': 'Ativo',
        }