from django.shortcuts import render, get_object_or_404, redirect
from requisicao.models import Cadastro_Requisicao, Item_requisicao
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RequisicaoForm, ItemForm
from django.db.models import Q
from django.contrib import messages
import csv
import xlwt
from django.http import HttpResponse

### VIEWS REQUISICAO ####

@login_required(login_url='/entrar')
def requisicao(request):
    context = {
        'titulo': 'Requisições'
    }
    return render(request, 'requisicao/requisicao.html', context)

@login_required(login_url='/entrar')
def lista_requisicao(request, id=None, id_req=None ):
    pesquisa = request.GET.get("pesquisa", None)    
    if pesquisa:
        list_requisicao = Cadastro_Requisicao.objects.all()
        # Icontains é como se fosse um like%% do SQL
        list_requisicao = list_requisicao.filter(
            Q(Tipo_Req__icontains=pesquisa) |
            Q(id__icontains=pesquisa) |
            Q(Modelo__icontains=pesquisa)
        )
    else:
        list_requisicao = Cadastro_Requisicao.objects.all()
        itens = Item_requisicao.objects.filter(Requisicao=id_req)
    context = {
        'list_requisicao': list_requisicao,
        'list_itens': itens
    }
    return render(request, "requisicao/lista-requisicao.html", context)



@login_required(login_url='/entrar')
def cadastrar_requisicao(request):
    list_requisicao = Cadastro_Requisicao.objects.all()
    if request.method == "POST":
        form = RequisicaoForm(request.POST)
        if form.is_valid():
            requisicao = form.save(commit=False)
            requisicao.username = request.user
            requisicao.save()
            return redirect('requisicao:lista-requisicao')
    else:
        form = RequisicaoForm()
    context = {
        "form": form
    }
    return render(request, "requisicao/cadastrar-requisicao.html", context)

@login_required(login_url='/entrar')
def atualiza_requisicao(request, id):
    req = get_object_or_404(Cadastro_Requisicao, pk=id)
    form = RequisicaoForm(request.POST or None,
                     request.FILES or None, instance=req)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('requisicao:lista-requisicao')
    return render(request, "requisicao/cadastrar-requisicao.html", context)


@login_required(login_url='/entrar')
def excluir_requisicao(request, id):
    placa = get_object_or_404(Cadastro_Requisicao, id=id)
    context = {
        "requisicao": Cadastro_Requisicao.objects.filter(id=id)[0]
    }
    if request.method == "POST":
        placa.delete()
        return redirect('requisicao:lista-requisicao')
    return render(request, "requisicao/excluir-requisicao.html", context)


@login_required(login_url='/entrar')
def cadastrar_item_requisicao(request, id_req):
    list_item = Item_requisicao.objects.all()
    req = Cadastro_Requisicao.objects.filter(id=id_req).first()
    qtd_atendida = Item_requisicao.objects.filter(Requisicao_id=id_req).count()
    qtd_requerida = req.Qtd_requerida
    if qtd_requerida == qtd_atendida:
        ds = True
        descricao = True
    else:
        ds = False
        descricao = False
    if request.method == "POST":
        form = ItemForm(request.POST, id_form = id_req, disable_serie = ds, disable_descricao = descricao)      
        if form.is_valid():
            if form.cleaned_data['Numero_serie'].Modelo == req.Modelo:
                item = form.save(commit=False)
                item.username = request.user
                item.Requisicao = req
                item.save()
                return redirect('requisicao:lista-requisicao')
            else:
                messages.error(request, 'Modelo diferente do requisitado!')
    else:
        form = ItemForm(id_form = id_req, disable_serie = ds, disable_descricao = descricao)
    context = {
        "form": form,
        "requisicao": req,
        "qtd_atendida": qtd_atendida,
        "qtd_requerida": qtd_requerida,
        "qtd_pendente": qtd_requerida - qtd_atendida,
        "percentual_int": int(qtd_atendida/qtd_requerida*100),
        "percentual_float": round(qtd_atendida/qtd_requerida*100, 1)
        }
    return render(request, "requisicao/cadastrar-item-requisicao.html", context)


# ------------------- Exportar para CSV ---------------------#


def ExportarRequisicaoCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="RequisicaoCadastradas.csv"'

    requisicao = Cadastro_Requisicao.objects.filter()

    writer = csv.writer(response)
    writer.writerow(['Tipo de Req','Modelo','Qtd.Requerida','Qtd.Atendida','Status','Descricao','Data_requisicao','Data_alteracao_requisicao','username'])

    for registro in requisicao:
        writer.writerow([registro.Tipo_Req, 
                        registro.Modelo,
                        registro.Qtd_requerida,
                        registro.Qtd_atendida,
                        registro.Status,
                        registro.Descricao,
                        registro.Data_requisicao,
                        registro.Data_alteracao_requisicao,
                        registro.username,
                        ])
    return response