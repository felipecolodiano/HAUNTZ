from django import forms
from .models import *


class FormTeste(forms.ModelForm):
    class Meta:
        model = Teste
        fields = '__all__'

    def __init__(self, *args, **kwargs ):
        self.status = kwargs.pop('status')
        self.etapa = kwargs.pop('etapa')   
        super(FormTeste, self).__init__(*args, **kwargs)
        self.fields['Status'].disabled = True
        self.fields['Status'].initial = self.status
        self.fields['Etapa_teste'].disabled = True
        self.fields['Etapa_teste'].initial = self.etapa
