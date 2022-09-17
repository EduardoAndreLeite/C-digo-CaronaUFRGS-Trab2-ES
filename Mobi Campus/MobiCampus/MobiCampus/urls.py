from unittest import result
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('<str:usuario_login>/', views.detail, name='detail'),
    path('<str:usuario_login>/motorista/', views.motorista, name='motorista'),
    path('<str:usuario_login>/motorista/adiciona_viagem', views.CriarNovaCarona, name='criarnovacarona'),
    path('<str:usuario_login>/buscando_viagem/', views.buscando_viagem, name='viagem'),
    path('<str:usuario_login>/historico_viagem/', views.historico_viagem, name='historico'),
]