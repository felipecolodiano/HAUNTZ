from django.contrib import admin
from requisicao.models import Cadastro_Requisicao, Item_requisicao

class MenuRequisicaoAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Caminho')

class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('Tipo_Req', 'Modelo' )

class ItensRequisicaoAdmin(admin.ModelAdmin):
    list_display = ('Numero_serie',)

admin.site.register(Cadastro_Requisicao, RequisicaoAdmin)
admin.site.register(Item_requisicao, ItensRequisicaoAdmin)

