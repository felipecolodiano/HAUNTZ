from django.urls import path
from requisicao import views

app_name = 'requisicao'

urlpatterns = [
    path('lista-requisicao/', views.lista_requisicao, name="requisicao"),
    path('cadastrar-requisicao/', views.cadastrar_requisicao, name="cadastrar-requisicao")
    ]