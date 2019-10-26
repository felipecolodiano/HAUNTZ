from django.db import models
from django.db.models import constraints
from placas.models import modelo_placas, cadastro_lote
from requisicao.models import requisicao
from testes.models import menu_testes

STATUS_CHOICES = (  
    ("Pedente", "Pedente"),
    ("Em andamento","Em andamento"),
    ("Finalizado", "Finalizado")
)

SITUACAO_CHOICES = (  
    ("Em andamento", "Em andamento"),
    ("Aprovado","Aprovado"),
    ("Reprovado","Reprovado")
)

ETAPA_CHOICES = (  
    ("Burn in","Burn in"),
    ("Teste 2","Teste 2"),
    ("Teste Final","Teste Final")
)

class Teste(models.Model):
    Etapa_teste = models.CharField(
        'Etapa do teste',
        choices=ETAPA_CHOICES
    )
    
    Requisicao = models.ForeignKey(
        'requisicao.requisicao',
        on_delete=models.CASCADE,
        related_name='Requisicao_Id_Requisicao'
    )

    Descricao = models.CharField(
        'Teste de Burning',
        max_length=30
    )

    Lote_numero = models.ForeignKey(
        'placas.cadastro_lote', 
        on_delete=models.CASCADE, 
        related_name='Cadastro_numero_lote',
        limit_choices_to= {'Ativo': True} #Limita somente a modelos ativos
    )
    
    Inicio = models.DateTimeField(
        'Data Início',
        auto_now=True
    )    
    
    Fim = models.DateTimeField(
        'Data Fim',
    )

    Status = models.CharField(
        'Status Teste',
        choices=STATUS_CHOICES
    )

    Situacao = models.CharField(
        'Situaçao do teste',
        choices=SITUACAO_CHOICES
    ) 

    Observacao = models.CharField(
        'Observação', 
        max_length=100
    )

    def __str__(self):
        return self.Etapa_teste

