from django.urls import path
from indicadores import views

app_name = 'indicadores'
urlpatterns = [
    path('requisicao/', views.indicadores_requisicao, name="indicadores-requisicao"),
    path('teste/', views.indicadores_teste, name="indicadores-teste")
]

