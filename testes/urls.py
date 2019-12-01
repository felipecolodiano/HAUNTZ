from django.urls import path
from testes import views

app_name = 'testes' 

urlpatterns = [
    path('', views.lista_testes, name="lista-itens-teste"),
    path('<int:id_item>', views.realiza_teste, name="realiza-teste" )
    ]