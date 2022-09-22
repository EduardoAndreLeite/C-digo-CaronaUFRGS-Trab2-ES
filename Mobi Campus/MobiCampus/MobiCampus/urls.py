from unittest import result
from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('home', views.detail, name='detail'),
    path('motorista/', views.motorista, name='motorista'),
    path('motorista/adiciona_viagem', views.CriarNovaCarona, name='criarnovacarona'),
    path('buscando_viagem/', views.buscando_viagem, name='viagem'),
    path('historico_viagem/', views.historico_viagem, name='historico'),
]