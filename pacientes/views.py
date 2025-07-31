from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Pacientes, Consultas, Visualizacoes
from django.contrib import messages
from django.contrib.messages import constants
from .forms import PacienteForm, ConsultaForm
from django.contrib import messages
from django.contrib.messages import constants, get_messages
from django.db.models import Q
from django.core.exceptions import ValidationError
import re
from collections import Counter
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
import secrets
from django.core.mail import send_mail
from django.utils.http import urlencode
import datetime

def home(request):
    return render(request, 'home.html')

def pacientes(request):
    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES)
        
        if form.is_valid():
            paciente_nome = form.cleaned_data['paciente_nome']
            paciente_email = form.cleaned_data['paciente_email']
            paciente_telefone = form.cleaned_data['paciente_telefone']
            
            paciente_existente = Pacientes.objects.filter(
                paciente_nome=paciente_nome
            ).union(
                Pacientes.objects.filter(paciente_email=paciente_email),
                Pacientes.objects.filter(paciente_telefone=paciente_telefone)
            ).first()

            if paciente_existente:
                messages.error(request, 'Nome, e-mail ou telefone já cadastrados.')
                return redirect('pacientes')
            
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso.')
            return redirect('pacientes')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
            return redirect('pacientes')

    else:
        form = PacienteForm()
        pacientes = Pacientes.objects.all()
        show_pacientes = Pacientes.objects.order_by('-id')[:4]
        return render(request, 'pacientes.html', {
            'form': form,
            'paciente_queixas': Pacientes.queixa_choices, 
            'pacientes': pacientes, 
            'show_pacientes': show_pacientes,
        })
    

def paciente_registro(request, id):
    paciente = Pacientes.objects.get(id=id)
    
    if request.method == "GET":
        consultas = Consultas.objects.filter(paciente=paciente).order_by('-paciente_data')
        total_consultas = consultas.count()
        tuple_grafico = (
            [str(i.paciente_data) for i in consultas.order_by('paciente_data')],
            [str(i.paciente_humor) for i in consultas.order_by('paciente_data')]
        )
        form = ConsultaForm()
        
        return render(request, 'paciente.html', {
            'paciente': paciente,
            'consultas': consultas,
            'tarefas': Consultas.tarefa_choices,
            'frequencia': Consultas.frequencia_choices,
            'tuple_grafico': tuple_grafico,
            'total_consultas': total_consultas,
            'form': form,
        })
    
    elif request.method == "POST":
        form = ConsultaForm(request.POST, request.FILES)
        
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            messages.success(request, 'Registro adicionado com sucesso.')
            return redirect(f'/pacientes/{id}')
        else:
            consultas = Consultas.objects.filter(paciente=paciente).order_by('-paciente_data')
            total_consultas = consultas.count()
            tuple_grafico = (
                [str(i.paciente_data) for i in consultas.order_by('paciente_data')],
                [str(i.paciente_humor) for i in consultas.order_by('paciente_data')]
            )
            messages.error(request, 'Erro no formulário. Por favor, corrija os campos abaixo.')
            return render(request, 'paciente.html', {
                'paciente': paciente,
                'consultas': consultas,
                'tarefas': Consultas.tarefa_choices,
                'frequencia': Consultas.frequencia_choices,
                'tuple_grafico': tuple_grafico,
                'total_consultas': total_consultas,
                'form': form,
            })
    
def atualizar_paciente(request, id):
    paciente_pagamento_em_dia = request.POST.get('paciente_pagamento_em_dia')
    paciente = Pacientes.objects.get(id=id)
    
    status = True if paciente_pagamento_em_dia == 'ativo' else False
    paciente.paciente_pagamento_em_dia = status
    paciente.save()
    
    return redirect(f'/pacientes/{id}')

def excluir_consulta(request,id):
    consulta = Consultas.objects.get(id=id)
    consulta.delete()
    return redirect(f'/pacientes/{consulta.paciente.id}')

def consulta_publica(request,id):
    consulta = Consultas.objects.get(id=id)
    if not consulta.paciente.paciente_pagamento_em_dia:
        raise Http404()
    
    Visualizacoes.objects.create(
        consulta=consulta,
        ip=request.META.get('REMOTE_ADDR', '0.0.0.0')
    )
    
    return render(request, 'consulta_publica.html', {'consulta' : consulta})

def excluir_paciente(request,id):
    paciente = Pacientes.objects.get(id=id)
    paciente.delete()
    return redirect(f'/pacientes/')
