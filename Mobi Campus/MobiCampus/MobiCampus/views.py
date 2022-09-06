from multiprocessing import context
from django.shortcuts import render, get_object_or_404,get_list_or_404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Usuario, Administrador, Motorista, Carona, CaronaAux
from django.template import loader
from django.http import Http404
from .forms import Autenticacao, Pedido

#Responsavel pela view da pagina inicial
def index(request):
    if(request.method=='POST'):
        form=Autenticacao(request.POST)

        if(form.is_valid()):
            nome=form.cleaned_data['login']
            password=form.cleaned_data['senha']
            user=get_object_or_404(Usuario, pk=nome)
            
            if(user.senha==password):
                return HttpResponseRedirect(nome)
            else:
                error= loader.get_template('MobiCampus/index.html')
                contexto={
                    'form': form,
                    'erro': True,
                }
                return HttpResponse(error.render(contexto, request))
    else:
        form=Autenticacao()    
    
    template = loader.get_template('MobiCampus/index.html')
    contexto= {
        'form': form,
        'erro': False,
        }

    return HttpResponse(template.render(contexto, request))


#Responsável pela view da pagina do usuario
def detail(request, usuario_login):
    user=get_object_or_404(Usuario, pk=usuario_login)
    
    template = loader.get_template('MobiCampus/detail.html')
    contexto={
        'user':user,
    }

    return HttpResponse(template.render(contexto, request))

#Responsavel pela view da página de um motorista
def motorista(request, usuario_login):
    user=get_object_or_404(Usuario, pk=usuario_login)

    return HttpResponse(user.nome)


#responsável pela view da página de busca 
def buscando_viagem(request, usuario_login):
    if(request.method=='POST'):
        form=Pedido(request.POST)

        if(form.is_valid()):
            origem=form.cleaned_data['origem']
            destino=form.cleaned_data['destino']

            return HttpResponseRedirect(origem+"+"+destino)
    else:
        form=Pedido(request.POST)
    
    template = loader.get_template('MobiCampus/buscar_viagem.html')

    contexto={
        'form':form,
    }
    return HttpResponse(template.render(contexto, request))

def resultado(request, usuario_login, busca):
    
    origem, destino= busca.split('+')
    
    #regex para achar uma rota que contenha a origem e destino nesta ordem
    matcher='[a-zA-Z ,]*'+origem+'[a-zA-Z ,]*'+destino+'[a-zA-Z ,]*'

    caronas=Carona.objects.filter(rota__regex=matcher, passageiros__lt=4).values()

    template=loader.get_template('MobiCampus/resultados_busca.html')

    contexto={
        'resultados_list':caronas,
    }
    
    return HttpResponse(template.render(contexto, request))

#responsável pela view do historico de viagens 
def historico_viagem(request, usuario_login):

    caronas = CaronaAux.objects.filter(passageiro_id=usuario_login).values()
    setOfCaronaIds = [carona['carona_id'] for carona in caronas]
    viagens = []
    for id in setOfCaronaIds:
        viagens.append(Carona.objects.filter(caronaId = id).values()[0])

    contexto={
        'historico_list':viagens,
    }
    
    template=loader.get_template('MobiCampus/historico_viagem.html')
    return HttpResponse(template.render(contexto, request))
