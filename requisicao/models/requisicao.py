from django.db import models
from django.db.models import constraints
from placas.models import cadastro_lote
from requisicao.models import menu_requisicao

TIPO_CHOICES = (
    ("Nova", "Nova"),
    ("Retorno", "Retorno")
)
STATUS_CHOICES = (
    ("Pendente", "Pendente"),
    ("Em Andamento", "Em Andamento"),
    ("Finalizado", "Finalizado")
)


class Cadastro_Requisicao(models.Model):
    Tipo_Req = models.CharField( #Tipo de Requisição
        'Tipo de requisicao',
        max_length=30,
        choices=TIPO_CHOICES
        )


    Modelo = models.ForeignKey( # Modelo
        'placas.modelo_placas', 
        related_name='Modelo_placas_modelo',
        on_delete = models.PROTECT,
        null = True,
        limit_choices_to= {'Ativo': True} #Limita somente a modelos ativos
    )

    Qtd_placa = models.IntegerField(
        'Qtd_de_Placas'
    )

    Status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES
    )

    #Id_Teste_01
    #Id_Teste_02
    #Id_Teste_03
    


    def __str__(self):
        return self.Tipo_Req

    class Meta:
        db_table = 'CADASTRO_REQUISICAO'
