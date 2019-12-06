import json
from django.shortcuts import render, get_object_or_404
from indicadores.models import Menu_indicadores
from requisicao.models import Cadastro_Requisicao, Item_requisicao
from django.contrib.auth.decorators import login_required, user_passes_test
#from placas.models import Teste
from datetime import datetime


@login_required
def indicadores_requisicao(request):
    queryset1 = Cadastro_Requisicao.objects.all()
    modelos = [str(obj.Modelo) for obj in queryset1]
    count_req = [int(obj.Qtd_requerida) for obj in queryset1]

    queryset2 = Cadastro_Requisicao.objects.all()
    status = [str(obj.Status) for obj in queryset2]
    count_aten = [int(obj.Qtd_atendida) for obj in queryset2]

    context = {
        'titulo1': "",
        'modelos': json.dumps(modelos),
        'requeridas': json.dumps(count_req),
        'titulo2':"",
        'status': json.dumps(status),
        'atendidas': json.dumps(count_aten)
    }
    
    return render(request, "indicadores/indicadores_requisicao.html", context)


