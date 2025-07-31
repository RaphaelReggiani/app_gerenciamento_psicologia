from django.db import models
from django.urls import reverse
from .choices import queixas, frequencia, tarefas
from .validators import name_validator, email_validator, phone_validator
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from collections import Counter

class Pacientes(models.Model):
    
    queixa_choices = queixas
    
    paciente_nome = models.CharField(max_length=255, unique=True, validators=[name_validator], help_text="Insira o nome completo.", error_messages={'unique': "Já existe um paciente cadastrado com esse nome."})
    paciente_email = models.EmailField(unique=True, validators=[email_validator], help_text="Insira o e-mail: exemplo@exemplo.com", error_messages={'unique': "E-mail já cadastrado."})
    paciente_telefone = models.CharField(unique=True, max_length=15, validators=[phone_validator], null=True, blank=True, help_text="(0XX)XXXXXXXXX", error_messages={'unique': "Número de telefone já castrado."})
    paciente_foto = models.ImageField(upload_to='fotos')
    paciente_pagamento_em_dia = models.BooleanField(default=True)
    paciente_queixa = models.CharField(max_length=5, choices=queixa_choices, default='Queixa', help_text="queixa")
    
    def __str__(self):
        return self.paciente_nome
    
class Consultas(models.Model):

    tarefa_choices = tarefas
    frequencia_choices = frequencia

    paciente_humor = models.PositiveIntegerField()
    paciente_registro_geral = models.TextField(null=True, blank=True)
    paciente_tarefa = models.CharField(max_length=55, choices=tarefa_choices, default='Tarefa', help_text="tarefa")
    paciente_frequencia = models.CharField(max_length=55, choices=frequencia_choices, default='Frequência', help_text="frequência")
    paciente_video = models.FileField(upload_to="video", null=True, blank=True)
    paciente_data = models.DateTimeField(auto_now_add=True)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)

    def __str__(self):
        return self.paciente.paciente_nome
    
    @property
    def link_publico(self):
        return f"http://127.0.0.1:8000{reverse('consulta_publica', kwargs={'id' : self.id})}"
    
    def views(self):
        return Visualizacoes.objects.filter(consulta=self).count()
    
class Visualizacoes(models.Model):
    consulta = models.ForeignKey(Consultas, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    
    