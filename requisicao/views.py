from django.shortcuts import render, get_object_or_404, redirect
from requisicao.models import Cadastro_Requisicao
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RequisicaoForm
from django.db.models import Q


### VIEWS MODELO ####

@login_required
def lista_requisicao(request, id=None):
    pesquisa = request.GET.get("pesquisa", None)
    if pesquisa:
        list_requisicao = Cadastro_Requisicao.objects.all()
        list_requisicao = list_requisicao.filter(
            Q(Tipo_Req__icontains=pesquisa)
        )  # Icontains é como se fosse um like%% do SQL
    else:
        list_requisicao = Cadastro_Requisicao.objects.all()
    context = {
        'list_requisicao': list_requisicao
    }
    return render(request, "requisicao/requisicao.html", context)


@login_required
def cadastrar_requisicao(request):
    list_requisicao = Cadastro_Requisicao.objects.all()
    context = {
        "form": RequisicaoForm,
        "list_requisicao": list_requisicao
    }
    if request.method == "POST":
        form = RequisicaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('requisicao:requisicao')
    return render(request, "requisicao/cadastrar-requisicao.html", context)