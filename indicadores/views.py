from django.shortcuts import render, get_object_or_404
from indicadores.models import Menu_indicadores
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def indicadores(request):
    context = {
        "titulo": ""

    }
    
    return render(request, "indicadores/indicadores_requisicao.html", context)