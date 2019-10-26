from django import forms
from .models import *

class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Cadastro_Requisicao
        fields = '__all__'
