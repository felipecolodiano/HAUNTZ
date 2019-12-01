from django.shortcuts import render, get_object_or_404, redirect
from testes.models import Menu_testes, Teste
from django.contrib.auth.decorators import login_required, user_passes_test
from requisicao.models import Cadastro_Requisicao, Item_requisicao
from testes.forms import FormTeste
from datetime import datetime
from requisicao.forms import ItemForm


def lista_testes(request, id_item=None):
    itens_pendente = Item_requisicao.objects.filter(Status_teste='Pendente')
    itens_andamento = Item_requisicao.objects.filter(Status_teste='Em andamento')
    itens_finalizado = Item_requisicao.objects.filter(Status_teste='Finalizado')
    context = {
        'titulo': 'Testes',
        'item': "",
        'pendente': itens_pendente,
        'andamento': itens_andamento,
        'finalizado': itens_finalizado
    }
    
    return render(request, "testes/lista-itens-teste.html", context)


@login_required(login_url='/entrar')
def realiza_teste(request, id_item=None):
    item = Item_requisicao.objects.get(id=id_item)
    itens_pendente = Item_requisicao.objects.filter(Status_teste='Pendente')
    itens_andamento = Item_requisicao.objects.filter(Status_teste='Em andamento')
    itens_finalizado = Item_requisicao.objects.filter(Status_teste='Finalizado')
       
    Status = item.Status_teste 
    
    #Valida o campo etapa do teste
    Etapa = item.Etapa_teste
    if Etapa == 'Pendente':
        Etapa = 'Burn In'
    elif Etapa == 'Burn In':
        Etapa = 'Pre-Teste'
    else:
        Etapa = 'Teste Final'

    if request.method == "POST":
        form = FormTeste(request.POST, status = Status, etapa = Etapa)
        if form.is_valid():
            teste = form.save(commit=False)
            teste.username = request.user
            teste.Item_requisicao = item
            teste.Etapa_testa = Etapa
            if teste.Etapa_teste == 'Teste Final':
                teste.Status = 'Finalizado'
                teste.Fim = datetime.now()
            else:
                teste.Status = 'Em andamento'
            if form.cleaned_data['Situacao'].upper() == "APROVADO":
                if teste.Status != 'Finalizado':
                    item.Status_teste = 'Em andamento'
                else:
                    item.Status_teste = 'Finalizado'
            item.Etapa_teste = Etapa
            item.save()
            teste = form.save()
            return redirect('testes:lista-itens-teste')
    form = FormTeste(status = Status, etapa = Etapa)
    context = {
        'titulo': 'Teste do item: ' + str(item.Numero_serie).split()[0],
        'form':form,
        'item': item,
        'pendente': itens_pendente,
        'andamento': itens_andamento,
        'finalizado': itens_finalizado
    }
    return render(request, "testes/lista-itens-teste.html", context)