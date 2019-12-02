from django import forms
from .models import *

class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Cadastro_Requisicao
        fields = '__all__'


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item_requisicao
        fields = '__all__'

    def __init__(self, *args, **kwargs ):         
        self.id_form = kwargs.pop('id_form')
        self.disable_serie = kwargs.pop('disable_serie')
        self.disable_descricao = kwargs.pop('disable_descricao') 
        super(ItemForm, self).__init__(*args, **kwargs)    

        self.fields['Requisicao'].disabled = True        
        self.fields['Requisicao'].initial = self.id_form
        self.fields['Numero_serie'].disabled = self.disable_serie
        self.fields['Descricao'].disabled = self.disable_descricao
