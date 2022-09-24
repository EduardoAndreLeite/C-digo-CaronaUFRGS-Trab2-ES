from unicodedata import name
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class Autenticacao(forms.Form):
    login=forms.CharField(label='Login', 
                          required=True,
                          max_length=150)
    senha=forms.CharField(label='Senha',
                          required=True,
                          max_length=None)

def validate_dominio_ufrgs(mail):
    import re
    if re.search(r"@ufrgs.br$", mail) is None:
        raise ValidationError(('Email deve possuir dominio UFRGS'), code='bad_dominio')

def validate_unique(mail):
    from django.contrib.auth.models import User
    if len(User.objects.filter(username=mail)) > 0:
        raise ValidationError(('Email já cadastrado'), code='username_taken')


class Cadastro(forms.Form):
    primeiro_nome = forms.CharField(label='Nome',
                                    max_length=150,
                                    required=False)
    sobrenome = forms.CharField(label='Sobrenome',
                                max_length=150,
                                required=False)
    login=forms.CharField(label='Login', 
                          required=True,
                          max_length=150,
                          validators=[validate_email, validate_dominio_ufrgs, validate_unique])
    senha=forms.CharField(label='Senha',
                          required=True,
                          max_length=None)
    cnh=forms.CharField(label='CNH',
                        required=False,
                        max_length=None)

    motorista_check=forms.BooleanField(label='Desejo me cadastrar como motorista',
                                       required=False)

class Pedido(forms.Form):
    origem=forms.CharField(label='Origem', max_length=50)
    destino=forms.CharField(label='Destino', max_length=50)
    tempo=forms.IntegerField(label='tempo')

class InsercaoViagem(forms.Form):
    origem=forms.CharField(label='Origem', max_length=50)
    destino=forms.CharField(label='Destino', max_length=50)
    tempo=forms.IntegerField(label='Tempo')

