from django.db import models
from django.db.models import constraints
from placas.models import cadastro_lote,cadastro_placas, modelo_placas
from contas.models import Usuario
from requisicao.models import menu_requisicao
from testes.models import Teste
from datetime import datetime

class Cadastro_Requisicao(models.Model):
    TIPO_CHOICES = (
        ("Nova", "Nova"),
        ("Retorno", "Retorno")
    )
   
    STATUS_CHOICES = (
        ("Pendente", "Pendente"),
        ("Em Andamento", "Em Andamento"),
        ("Finalizado", "Finalizado")
    )

    Tipo_Req = models.CharField( #Tipo de Requisição
        'Tipo de requisicao',
        max_length=30,
        choices=TIPO_CHOICES
        )

    Modelo = models.ForeignKey( # Modelo
        'placas.modelo_placas', 
        related_name='Modelo_placas_modelo',
        on_delete = models.PROTECT,
        limit_choices_to= {'Ativo': True} #Limita somente a modelos ativos
    )

    Qtd_requerida = models.IntegerField(
        'Qtd Requerida'
    )

    Qtd_atendida = models.IntegerField(
        'Qtd Atendida',
        default = int(),
        editable = False
    )

    Status = models.CharField(
        default="Pendente"
        'Status',
        max_length=20,
        choices=STATUS_CHOICES
    )

    Descricao = models.TextField(
        'Descrição da requisição'
    )

    Data_requisicao = models.DateTimeField(
        auto_now_add = True
    )

    Data_alteracao_requisicao = models.DateTimeField(
        auto_now = True
    )

    username = models.ForeignKey(
        'contas.usuario',
        related_name='contas_usuario_username_requisicao',
        on_delete=models.PROTECT,
        editable = False,
        default = ""
    )
    
    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        db_table = 'CADASTRO_REQUISICAO'


class Item_requisicao(models.Model):
    Numero_serie = models.OneToOneField(
        'placas.cadastro_placas',
        verbose_name = 'Número de Série',
        related_name='cadastro_placas_numero_serie',
        on_delete=models.PROTECT,
        null = False,
        blank = False
    )

    Descricao = models.CharField(
        'Descrição do item',
        max_length = 100,
        blank = True
    )

    Requisicao = models.ForeignKey(
        'requisicao.cadastro_requisicao',
        verbose_name = 'Requisição',
        related_name='cadastro_requisicao_id',
        on_delete = models.PROTECT     
    )

    Etapa_teste = models.CharField( 
        'Etapa do Teste',
        blank = True,
        null = True,
        max_length = 20,
        default='Pendente'
    )

    Status_teste = models.CharField(
        'Status do teste',
        blank = True,
        null = True,
        max_length = 20,
        default='Pendente'
    )
    
    Situacao_teste = models.CharField(
        'Status do teste',
        blank = True,
        null = True,
        max_length = 20,
        default=''
    )

    Data_item = models.DateTimeField(
        auto_now_add = True
    )

    username = models.ForeignKey(
        'contas.usuario',
        related_name='contas_usuario_username_item',
        on_delete = models.PROTECT,
        editable = False,
        default = "",
        null = True
    )

    def __str__(self):
        return '{} - {}'.format(self.Numero_serie, self.Numero_serie.Modelo)

    class Meta:
        db_table = 'ITEM_REQUISICAO'

