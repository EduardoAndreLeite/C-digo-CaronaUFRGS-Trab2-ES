from unicodedata import name
from django import forms

class Autenticacao(forms.Form):
    login=forms.CharField(label='Login', 
                          required=True,
                          max_length=150)
    senha=forms.CharField(label='Senha',
                          required=True,
                          max_length=None)

class Cadastro(forms.Form):
    primeiro_nome = forms.CharField(label='Nome',
                                    max_length=150,
                                    required=True)
    sobrenome = forms.CharField(label='Sobrenome',
                                max_length=150,
                                required=True)
    login=forms.CharField(label='Login', 
                          required=True,
                          max_length=150)
    senha=forms.CharField(label='Senha',
                          required=True,
                          max_length=None)
    confirmacao_senha=forms.CharField(label='Confirmação da senha',
                                      required=True,
                                      max_length=None)

class Pedido(forms.Form):
    origem=forms.CharField(label='Origem', max_length=50)
    destino=forms.CharField(label='Destino', max_length=50)
    tempo=forms.IntegerField(label='tempo')

class InsercaoViagem(forms.Form):
    origem=forms.CharField(label='Origem', max_length=50)
    destino=forms.CharField(label='Destino', max_length=50)

