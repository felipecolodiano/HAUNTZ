from django.urls import path
from requisicao import views

app_name = 'requisicao'

#Urls Requisicao
urlpatterns = [
    path('', views.requisicao, name="requisicao"),
    path('lista-requisicao/', views.lista_requisicao, name="lista-requisicao"),
    path('lista-requisicao/detail/<int:id_req>', views.lista_requisicao, name="lista-requisicao-detail"),
    path('cadastrar-requisicao/', views.cadastrar_requisicao, name="cadastrar-requisicao"),
    path('cadastrar-item/<int:id_req>', views.cadastrar_item_requisicao, name="cadastrar-item-requisicao"),
    path('atualiza-requisicao/<int:id>', views.atualiza_requisicao, name="atualiza-requisicao"),
    path('excluir-requisicao/<int:id>', views.excluir_requisicao, name="excluir-requisicao")
    ]