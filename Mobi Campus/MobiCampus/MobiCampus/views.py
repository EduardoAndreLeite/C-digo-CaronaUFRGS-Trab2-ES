from multiprocessing import context
from random import randint, random
from django.shortcuts import render, get_object_or_404,get_list_or_404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Usuario, Administrador, Motorista, Carona, CaronaHist
from django.template import loader
from django.http import Http404
from .forms import Autenticacao, Pedido, InsercaoViagem
from django.contrib.auth import authenticate, login

ORIGENSEDESTINOS=['Campus do Vale', 'Campus Centro', 'Campus Olimpico', 'Campus Saude']
RUAS=['Bento Goncalvez', 'Ipiranga', 'Dr.Salvador Franca', 'Borges de Medeiros']

#Responsavel pela view da pagina inicial
def login_page(request):
    if request.method=='POST':
        form=Autenticacao(request.POST)

        if(form.is_valid()):
            username=form.cleaned_data['login']
            password=form.cleaned_data['senha']
            user=authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('home')
            else:
                error= loader.get_template('MobiCampus/index.html')
                contexto={
                    'form': form,
                }
                return HttpResponse(error.render(contexto, request))
    else:
        form=Autenticacao()    
    
        template = loader.get_template('MobiCampus/login.html')
        contexto= {
            'form': form,
        }

    return HttpResponse(template.render(contexto, request))


#Responsável pela view da pagina do usuario
from django.contrib.auth.decorators import login_required

@login_required
def detail(request):
    template = loader.get_template('MobiCampus/detail.html')
    contexto={
        'user':request.user,
    }

    return HttpResponse(template.render(contexto, request))

#Responsavel pela view da página de um motorista
@login_required
def motorista(request):
    user=request.user

    return HttpResponse(user.get_username())


#responsável pela view da página de busca 
@login_required
def buscando_viagem(request):
    if(request.method=='POST'):
        form=Pedido(request.POST)

        if(form.is_valid()):
            origem=form.cleaned_data['origem']
            destino=form.cleaned_data['destino']
            tempo=form.cleaned_data['tempo']

            return resultado(request, origem+'+'+destino, tempo)
    else:
        form=Pedido(request.POST)
    
    template = loader.get_template('MobiCampus/buscar_viagem.html')

    contexto={
        'form':form,
    }
    return HttpResponse(template.render(contexto, request))

def resultado(request, busca, tempo):
    
    origem, destino= busca.split('+')
    
    #regex para achar uma rota que contenha a origem e destino nesta ordem
    matcher='[a-zA-Z ,]*'+origem+'[a-zA-Z ,]*'+destino+'[a-zA-Z ,]*'

    caronas=Carona.objects.filter(rota__regex=matcher, passageiros__lt=4).values()
    caronas.filter(tempo__lte=tempo)
    template=loader.get_template('MobiCampus/resultados_busca.html')

    contexto={
        'resultados_list':caronas,
    }
    
    return HttpResponse(template.render(contexto, request))

#Devolve uma rota aleatória
def randomizador_rota(origem, destino):
    maximo=len(RUAS)-1
    rota=origem+' ,'+RUAS[randint(0, maximo)]+' ,'+RUAS[randint(0, maximo)]+' ,'+destino

    return rota

#Realiza a inserção de uma viagem no sistema
def CriarNovaCarona(request, usuario_login):
    template=loader.get_template('MobiCampus/CriaNovaCarona.html')  
    
    if(request.method=='POST'):
        form=InsercaoViagem(request.POST)

        if(form.is_valid()):
           origem=form.cleaned_data['origem']
           destino=form.cleaned_data['destino']
           rota=randomizador_rota(origem, destino)

           if (origem in ORIGENSEDESTINOS and destino in ORIGENSEDESTINOS):
                viagem=Carona(origem=origem, destino=destino, rota=rota, tempo=randint(0,90), motorista=get_object_or_404(Motorista, pk=usuario_login), custo=randint(1, 25))
                viagem.save()
                hist_inst=CaronaHist(user=get_object_or_404(Usuario, pk=usuario_login), carona=viagem.caronaId, status='Passageiro')
                hist_inst.save()
                
                context=  { 
                    'form': form,
                    'comecado':True,
                    'erro': False, 
                    }

                return HttpResponse(template.render(context, request))
           else:
                context=  { 
                    'form': form,
                    'comecado':False,
                    'erro': False, 
                    }
                return HttpResponse(template.render(context, request))
    else:
        form=InsercaoViagem()
  
    context=  { 
        'form': form,
        'comecado':False,
        'erro': False, 
        }

    return HttpResponse(template.render(context, request))

#responsável pela view do historico de viagens 
@login_required
def historico_viagem(request):
    user = request.user
    caronas = CaronaHist.objects.filter(user=user.usuario).values()
    setOfCaronaIds = [carona['carona_id'] for carona in caronas]
    viagens = []
    for id in setOfCaronaIds:
        viagens.append(Carona.objects.filter(caronaId = id).values()[0])

    contexto={
        'historico_list':viagens,
    }
    
    template=loader.get_template('MobiCampus/historico_viagem.html')
    return HttpResponse(template.render(contexto, request))
