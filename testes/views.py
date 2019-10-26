from django.shortcuts import render, get_object_or_404
from testes.models import Menu_testes

def testes(request, caminho):
    teste = get_object_or_404(Menu_testes, Caminho = caminho)

    context = {
        "teste": teste
    }
    
    return render(request, "testes/testes.html", context)


def alterar_requisicao(reqeust, fase):

    context = {
        'titulo': 'testes fase' + fase
    }

    return render(reqeust, 'testes/testes_fase1.html', context)