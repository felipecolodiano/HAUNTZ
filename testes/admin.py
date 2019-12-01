from django.contrib import admin
from testes.models import Menu_testes, Teste


class MenuTestesAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Caminho')

class TestesAdmin(admin.ModelAdmin):
    list_display = ('Etapa_teste',)


admin.site.register(Menu_testes, MenuTestesAdmin)
admin.site.register(Teste, TestesAdmin)

