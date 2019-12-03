import json
from django.shortcuts import render, get_object_or_404
from indicadores.models import Menu_indicadores
from requisicao.models import Cadastro_Requisicao, Item_requisicao
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime




@login_required
def indicadores_requisicao(request):
    queryset = Cadastro_Requisicao.objects.all()
    modelos = [str(obj.Modelo) for obj in queryset]
    requeridas = [int(obj.Qtd_requerida) for obj in queryset]



    context = {
        'titulo': "",
        'modelos': json.dumps(modelos),
        'requeridas': json.dumps(requeridas)

    }
    
    return render(request, "indicadores/indicadores_requisicao.html", context)