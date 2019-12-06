from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required, user_passes_test
from requisicao.models import Cadastro_Requisicao, Item_requisicao
from placas.models import Cadastro_placas
from testes.models import Menu_testes, Teste
from testes.forms import FormTeste
from requisicao.forms import ItemForm
import csv
import xlwt
from django.http import HttpResponse

@login_required(login_url='/entrar')
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
    placa = Cadastro_placas.objects.get(id = item.Numero_serie.id)
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
            teste.Lote_numero = placa.Lote_numero
            if teste.Etapa_teste == 'Teste Final':
                teste.Status = 'Finalizado'
                teste.Fim = datetime.now()
            else:
                teste.Status = 'Em andamento'
            if form.cleaned_data['Situacao'].upper() == "APROVADO":
                if teste.Status != 'Finalizado':
                    item.Status_teste = 'Em andamento'
                    item.Situacao_teste = 'Aprovado'
                else:
                    item.Status_teste = 'Finalizado'
                    item.Situacao_teste = 'Aprovado'
            if form.cleaned_data['Situacao'].upper() == "REPROVADO":
                item.Status_teste = 'Finalizado'
                item.Situacao_teste = 'Reprovado'
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
        'finalizado': itens_finalizado,
        'placa': placa
    }
    return render(request, "testes/lista-itens-teste.html", context)


#--------------- Exportar Testes CSV ----------------------#

def ExportarTesteoCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="TestesCadastrados.csv"'

    testes = Teste.objects.filter()

    writer = csv.writer(response)
    writer.writerow(['Etapa_do_teste','Item_requisicao','Lote_numero','Data_teste','Fim','Status','Situacao','Observacao','Usuario'])

    for registro in testes:
        writer.writerow([registro.Etapa_teste, 
                        registro.Item_requisicao,
                        registro.Lote_numero,
                        registro.Data_teste,
                        registro.Fim,
                        registro.Status,
                        registro.Situacao,
                        registro.Observacao,
                        registro.username,
                        ])
    return response


import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def rel_teste(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="testes.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(210, 810, "RELATORIO DE TESTES - GERAL")

    testes = Teste.objects.all()

    str_ = ' %s      %s        %s       %s      %s        %s    '

    p.drawString(10,790, 'Etapa        |                              Item                        |         Lote        |     Data Fim     |      Status      |     Situacao     ')

    p.drawString(0, 810, "___" * 200)

    y= 750
    for test in testes:
        p.drawString(5, y, str_ % (test.Etapa_teste, test.Item_requisicao, test.Lote_numero, test.Fim, test.Status, test.Situacao))      
        y -= 22

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response
