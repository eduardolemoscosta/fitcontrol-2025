from django.contrib import admin
from .models import Aluno, Mensalidade, PlanoMensalidade


admin.site.register(Aluno)
admin.site.register(Mensalidade)
admin.site.register(PlanoMensalidade)