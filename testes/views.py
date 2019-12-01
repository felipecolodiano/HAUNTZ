from django.shortcuts import render, get_object_or_404
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
        'pendente': itens_pendente
    }
    
    return render(request, "testes/lista-itens-teste.html", context)

@login_required(login_url='/entrar')
def realiza_teste(request, id_item=None):
    item = Item_requisicao.objects.get(id=id_item)
    itens_pendente = Item_requisicao.objects.filter(Status_teste='Pendente')
    itens_andamento = Item_requisicao.objects.filter(Status_teste='Em andamento')
    itens_finalizado = Item_requisicao.objects.filter(Status_teste='Finalizado')
    if request.method == "POST":
        Status = item.Status_teste
        form = FormTeste(request.POST, status = Status, etapa = 'Burn In')
        form2 = ItemForm(request.POST, id_form = id_item)
        if form.is_valid():
            teste = form.save(commit=False)
            item = form2.save(commit=False)
            teste.username = request.user
            teste.Item_requisicao = id_item
            if teste.Etapa_teste == 'Teste Final':
                teste.Status = 'Finalizado'
                teste.Fim = datetime.now()
            else:
                teste.Status = 'Em andamento'
            item.Status_teste = teste.Status
            item.Etapa_teste = teste.Etapa_teste
            teste = form.save()
            item = form2.save() 
    Status = item.Status_teste
    form = FormTeste(status = Status, etapa = 'Burn In')
    context = {
        'titulo': 'Teste do item: ' + str(item.Numero_serie).split()[0],
        'form':form,
        'item': item,
        'pendente': itens_pendente
    }
    return render(request, "testes/lista-itens-teste.html", context)