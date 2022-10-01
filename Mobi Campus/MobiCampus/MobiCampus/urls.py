from unittest import result
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('cadastro', views.signup_page, name='signup_page'),
    path('home', views.detail, name='detail'),
    path('motorista/', views.motorista_detail, name='motorista'),
    path('motorista/adiciona_viagem', views.CriarNovaCarona, name='criarnovacarona'),
    path('buscando_viagem/', views.buscando_viagem, name='viagem'),
    path('historico_viagem/', views.historico_viagem, name='historico'),
    path('motorista/Em_Viagem/', views.Em_Viagem, name='Roaming' ),
    path('pedido/<int:carona>', views.Solicitar_Carona, name='pedido'),
    path('pedido/aguardando/', views.Aguardar, name='Aguardar'),
    path('motorista/viagem_finalizada', views.Finalizar_Carona, name='Finalizar'),
    path('motorista/viagem_finalizada_motorista', views.Finalizar_Carona_Motorista, name='FinalizarMotorista'),
    path('motorista/aceitar/<int:identificador>', views.Aceitar_Carona, name='Aceitar'),
    path('motorista/negar/<int:identificador>', views.Negar_Carona, name='Negar'),
    path('passageiro_em_viagem/', views.Viajando, name='Viajando'),
    path('avaliacao/', views.Avaliacao, name='Avaliacao'),
]