from django.shortcuts import render, get_object_or_404, redirect
from placas.models import Menu_placas, Modelo_placas, Cadastro_placas, Cadastro_lote
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ModeloForm, PlacaForm, LoteForm
from django.db.models import Q
import csv
import xlwt
from django.http import HttpResponse


### VIEWS MODELO ####

@login_required
def lista_modelo(request, id=None): # Lista Modelo
    pesquisa = request.GET.get("pesquisa", None)
    if pesquisa:
        list_modelo = Modelo_placas.objects.all()
        list_modelo = list_modelo.filter(
            Q(Modelo__icontains=pesquisa) |
            Q(Descricao__icontains=pesquisa) |
            Q(Ativo__icontains=pesquisa
              )
        )  # Icontains é como se fosse um like%% do SQL
    else:
        list_modelo = Modelo_placas.objects.all()
    context = {
        'list_modelo': list_modelo
    }
    return render(request, "placas/lista-modelo.html", context)


@login_required
def cadastrar_modelo(request): # Cadastrar Modelo
    list_modelo = Modelo_placas.objects.all()
    context = {
        "form": ModeloForm,
        "list_modelo": list_modelo
    }
    if request.method == "POST":
        form = ModeloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('placas:lista-modelo')
    return render(request, "placas/cadastrar-modelo.html", context)


@login_required
def excluir_modelo(request, id):#Excluir Modelo
    modelos = get_object_or_404(Modelo_placas, id=id)
    context = {
        "modelos": Modelo_placas.objects.filter(id=id)[0]
    }
    if request.method == "POST":
        modelos.delete()
        return redirect('placas:lista-modelo')
    return render(request, "placas/excluir-modelo.html", context)


@login_required
def atualiza_modelo(request, id):#Atualizar Modelo
    modelos = get_object_or_404(Modelo_placas, pk=id)
    form = ModeloForm(request.POST or None,
                      request.FILES or None, instance=modelos)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('placas:lista-modelo')
    return render(request, "placas/cadastrar-modelo.html", context)


########### VIEWS PLACA ##############

@login_required
def lista_placa(request, id=None):
    pesquisa = request.GET.get("pesquisa", None)
    if pesquisa:
        list_placa = Cadastro_placas.objects.all()
        list_placa = list_placa.filter(
            Q(Numero_serie__icontains=pesquisa) |
            Q(Observacao__icontains=pesquisa) |
            Q(Modelo__Modelo__icontains=pesquisa) 
            )  # Icontains é como se fosse um like%% do SQL
    else:
        list_placa = Cadastro_placas.objects.all()
    context = {
        'list_placa': list_placa
    }
    return render(request, "placas/lista-placa.html", context)


@login_required
def cadastrar_placa(request):
    if request.method == "POST":
        form = PlacaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('placas:lista-placa')
    else:
        form = PlacaForm()
    context = {
        "form": PlacaForm
    }
    return render(request, "placas/cadastrar-placa.html", context)


@login_required
def excluir_placa(request, id):
    placa = get_object_or_404(Cadastro_placas, id=id)
    context = {
        "placa": Cadastro_placas.objects.filter(id=id)[0]
    }
    if request.method == "POST":
        placa.delete()
        return redirect('placas:lista-placa')
    return render(request, "placas/excluir-placa.html", context)


@login_required
def atualiza_placa(request, id):
    placas = get_object_or_404(Cadastro_placas, pk=id)
    form = PlacaForm(request.POST or None,
                     request.FILES or None, instance=placas)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('placas:lista-placa')
    return render(request, "placas/cadastrar-placa.html", context)

############# VIEWS LOTE #############


@login_required
def lista_lote(request, id=None):
    pesquisa = request.GET.get("pesquisa", None)
    if pesquisa:
        list_lote = Cadastro_lote.objects.all()
        # Icontains é como se fosse um like%% do SQL
        list_lote = list_lote.filter(Lote_numero__icontains=pesquisa)
    else:
        list_lote = Cadastro_lote.objects.all()
    context = {
        'list_lote': list_lote
    }
    return render(request, "placas/lista-lote.html", context)





@login_required
def cadastrar_lote(request):
    list_lote = Cadastro_lote.objects.all()
    context = {
        "form": LoteForm,
        'list_lote': list_lote
    }
    if request.method == "POST":
        form = LoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('placas:lista-lote')
    return render(request, "placas/cadastrar-lote.html", context)


def excluir_lote(request, id):
    lote = get_object_or_404(Cadastro_lote, id=id)
    context = {
        "lote": Cadastro_lote.objects.filter(id=id)[0]
    }
    if request.method == "POST":
        lote.delete()
        return redirect('placas:cadastrar-lote')
    return render(request, "placas/excluir-lote.html", context)


@login_required
def atualiza_lote(request, id):
    lote = get_object_or_404(Cadastro_lote, pk=id)
    form = LoteForm(request.POST or None, request.FILES or None, instance=lote)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('placas:lista-lote')
    return render(request, "placas/cadastrar-lote.html", context)



#### EXPORTA CSV ####

def ExportarParaCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PlacasCadastradas.csv"'

    placas = Cadastro_placas.objects.filter()

    writer = csv.writer(response)
    writer.writerow(['Num.Serie', 'Modelo', 'Revisao_LM', 'Num. Lote', 'Observacao', 'Situacao'])
    
    for registro in placas:
        writer.writerow([registro.Numero_serie, 
                        registro.Modelo, registro.Revisao_lm, 
                        registro.Lote_numero, registro.Observacao, 
                        registro.Ativo
                        ])
    return response

#--------- Exportar MOdelo CSV ---------------#

def ExportarModeloCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ModelosCadastrados.csv"'

    placas = Modelo_placas.objects.filter()

    writer = csv.writer(response)
    writer.writerow(['Modelo', 'Descricao', 'Ativo'])

    for registro in placas:
        writer.writerow([registro.Modelo, 
                        registro.Descricao,
                        registro.Ativo
                        ])
    return response

#----------- Exportar Lote CSV ----------------#

def ExportarLoteCSV(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="LotesCadastrados.csv"'

    placas = Cadastro_lote.objects.filter()

    writer = csv.writer(response)
    writer.writerow(['Num.Lote','Ativo'])

    for registro in placas:
        writer.writerow([registro.Lote_numero, 
                        registro.Ativo
                        ])
    return response

'''
def ExportarParaCSV(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="PlacasCadastradas.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Cadastro de Placas')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Num.Serie', 'Modelo', 'Revisao_LM', 'Num. Lote', 'Observacao', 'Situacao']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    registros = Cadastro_placas.objects.all()

    #writer = csv.writer(response)
    #writer.writerow(['Num.Serie', 'Modelo', 'Revisao_LM', 'Num. Lote', 'Observacao', 'Situacao'])
    
    # for registro in placas:
    #     writer.writerow([registro.Numero_serie, 
    #                     registro.Modelo, registro.Revisao_lm, 
    #                     registro.Lote_numero, registro.Observacao, 
    #                     registro.Ativo
    #                     ])
    
    row_num = 1
    for registro in registros:
        ws.write(row_num, 0, registro.Numero_serie, font_style,)
        ws.write(row_num, 1, registro.Modelo, font_style,)
        ws.write(row_num, 2, registro.Revisao_lm, font_style,)
        ws.write(row_num, 3, registro.Lote_numero, font_style,)
        ws.write(row_num, 4, registro.Observacao, font_style,)
        ws.write(row_num, 5, registro.Ativo, font_style,)
        row_num += 1
        
    wb.save(response)
    return response
    '''

