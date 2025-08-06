from django.db import models
from django.urls import reverse
from .choices import queixas, frequencia, tarefas, dias, meses, anos, paises
from .validators import name_validator, email_validator, validate_password_rules, phone_validator, nickname_validator
from django.core.validators import MinLengthValidator, RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from collections import Counter


class NewUser(models.Model):
            
    user_pais_choices = paises
    user_dia_choices = dias
    user_mes_choices = meses
    user_ano_choices = anos

    user_psicologo_nickname = models.CharField(max_length=15, unique=True, validators=[nickname_validator], help_text="5-15 caracteres (apenas letras ou números).")
    user_psicologo_password = models.CharField(max_length=12, validators=[validate_password_rules], help_text="6-12 caracteres (incluir: 1 número e 1 caracter especial).")
    user_psicologo_nome = models.CharField(max_length=255, unique=True, validators=[name_validator], help_text="Insira o nome completo.", error_messages={'unique': "Já existe um paciente cadastrado com esse nome."})
    user_psicologo_email = models.EmailField(unique=True, validators=[email_validator], help_text="Insira o e-mail: exemplo@exemplo.com", error_messages={'unique': "E-mail já cadastrado."})
    user_psicologo_telefone = models.CharField(unique=True, max_length=15, validators=[phone_validator], null=True, blank=True, help_text="(0XX)XXXXXXXXX", error_messages={'unique': "Número de telefone já castrado."})
    user_psicologo_dia = models.CharField(max_length=12, choices=user_dia_choices, default='01', help_text="dia")
    user_psicologo_mes = models.CharField(max_length=12, choices=user_mes_choices, default='January', help_text="mês")
    user_psicologo_ano = models.CharField(max_length=12, choices=user_ano_choices, default='2025', help_text="ano")
    user_psicologo_pais = models.CharField(max_length=50, choices=user_pais_choices, help_text="Selecione seu país de origem")
    reset_token = models.CharField(max_length=64, blank=True)
    
    def save(self, *args, **kwargs):
        if self.user_psicologo_nome:
            self.user_psicologo_nome = ' '.join([w.capitalize() for w in self.user_psicologo_nome.strip().split()])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user_psicologo_nome

class Pacientes(models.Model):
    
    queixa_choices = queixas
    paciente_pais_choices = paises
    paciente_dia_choices = dias
    paciente_mes_choices = meses
    paciente_ano_choices = anos
    
    paciente_nome = models.CharField(max_length=255, unique=True, validators=[name_validator], help_text="Insira o nome completo.", error_messages={'unique': "Já existe um paciente cadastrado com esse nome."})
    paciente_email = models.EmailField(unique=True, validators=[email_validator], help_text="Insira o e-mail: exemplo@exemplo.com", error_messages={'unique': "E-mail já cadastrado."})
    paciente_telefone = models.CharField(unique=True, max_length=15, validators=[phone_validator], null=True, blank=True, help_text="(0XX)XXXXXXXXX", error_messages={'unique': "Número de telefone já castrado."})
    paciente_foto = models.ImageField(upload_to='fotos')
    paciente_pagamento_em_dia = models.BooleanField(default=True)
    paciente_queixa = models.CharField(max_length=15, choices=queixa_choices, default='Queixa', help_text="queixa")
    paciente_dia = models.CharField(max_length=12, null=True, blank=True, choices=paciente_dia_choices, default='01', help_text="dia")
    paciente_mes = models.CharField(max_length=12, null=True, blank=True, choices=paciente_mes_choices, default='January', help_text="mês")
    paciente_ano = models.CharField(max_length=12, null=True, blank=True, choices=paciente_ano_choices, default='2025', help_text="ano")
    paciente_pais = models.CharField(max_length=50, null=True, blank=True, choices=paciente_pais_choices, help_text="Selecione seu país de origem")

    paciente_ref_psicologo = models.ForeignKey(NewUser, on_delete=models.CASCADE, null=True, blank=True)
    
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
    
    