from django.contrib import admin
from requisicao.models import Cadastro_Requisicao

class MenuRequisicaoAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Caminho')

class RequisicaoAdmin(admin.ModelAdmin):
    list_display = ('Tipo_Req', )

#admin.site.register(Menu_requisicao, RequisicaoAdmin)
admin.site.register(Cadastro_Requisicao, RequisicaoAdmin)


