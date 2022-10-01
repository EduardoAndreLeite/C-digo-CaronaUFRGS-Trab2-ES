
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User, Group

max_passageiros=4
max_tam_string=50
max_tam_senha=20
tam_cnh=11
max_rota=300

class UserManager(models.Manager):
    def create_usuario(self, username, password, **kwargs):
        user = User.objects.create_user(username, 
                                        password=password)
        user.save()
        if "first_name" in kwargs.keys():
            user.first_name = kwargs["first_name"]
            user.save()
        if "last_name" in kwargs.keys():
            user.last_name = kwargs["last_name"]
            user.save()
        return self.create(user=user)
    def create_motorista(self, username, password, cnh, **kwargs):
        user = User.objects.create_user(username, 
                                        password=password)
        user.save()
        if 'first_name' in kwargs.keys():
            user.first_name = kwargs['first_name']
            user.save()
        if 'last_name' in kwargs.keys():
            user.last_name = kwargs['last_name']
            user.save()
        return self.create(user=user, cnh=cnh)

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numeros= ((1, '1'), (2,'2'), (3,'3'), (4,'4'), (5, '5'))
    aval=models.SmallIntegerField(default=5, choices=numeros)

    objects = UserManager()
    
    def __str__(self):
        return self.user.username

class Administrador(Usuario):
    permissao=models.BooleanField()

    def __str__(self):
        return super().__str__()


class Motorista(Usuario):
    cnh=models.CharField(max_length=tam_cnh)

    def __str__(self):
        return super().__str__()

class Carona(models.Model):
    motorista=models.ForeignKey(Motorista, on_delete=models.CASCADE)
    caronaId = models.AutoField(primary_key=True)
    origem=models.CharField(max_length=max_tam_string)
    tempo=models.IntegerField()
    destino=models.CharField(max_length=max_tam_string)
    rota=models.CharField(max_length=max_rota)
    custo=models.IntegerField()
    finalizada=models.BooleanField(default=False)
    passageiros=models.SmallIntegerField(default=0)


class CaronaHist(models.Model):
    carona=models.ForeignKey(Carona, on_delete=models.CASCADE)
    user=models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="user_profile")
    status=models.CharField(max_length=10)

class Solicitacao(models.Model):
    Motorista=models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name="Motorista")
    Passageiro=models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="Passageiro")
    Id=models.AutoField(primary_key=True)
    Carona=models.ForeignKey(Carona, on_delete=models.CASCADE)
    Aceito= models.BooleanField(default=False)

class Avaliacao(models.Model):
	rating = models.CharField(
	choices = ((u'1',u'Péssimo'),(u'2',u'Ruim'),(u'3',u'Regular'),(u'4',u'Bom'),(u'5',u'Ótimo')),
	max_length = 1,
	verbose_name = 'Avaliação'
	)


