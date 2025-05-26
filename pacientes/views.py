from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Pacientes, Tarefas, Consultas, Visualizacoes
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.

def home(request):
    return render(request, 'home.html')

def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.all()
        print(pacientes)
        return render(request, 'pacientes.html', {'queixas': Pacientes.queixa_choices, 'pacientes': pacientes})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        queixa = request.POST.get('queixa')
        foto = request.FILES.get('foto')
        
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(telefone.strip()) == 0 or not foto:
            messages.add_message(request, constants.ERROR, 'Todos os campos precisam ser preenchidos.')
            return redirect('pacientes')

        # Verificar se nome, email ou telefone já estão cadastrados
        paciente_existente = Pacientes.objects.filter(
            nome=nome
        ).union(
            Pacientes.objects.filter(email=email),
            Pacientes.objects.filter(telefone=telefone)
        ).first()

        if paciente_existente:
            messages.add_message(request, constants.ERROR, 'Nome, e-mail ou telefone já cadastrados.')
            return redirect('pacientes')
        
        paciente = Pacientes(
            nome=nome,
            email=email,
            telefone=telefone,
            queixa=queixa,
            foto=foto
        )
        
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(telefone.strip()) == 0 or not foto:
            messages.add_message(request, constants.ERROR, 'Todos os campos precisam ser preenchidos.')
            return redirect('pacientes')
        
        paciente.save()
        
        messages.add_message(request, constants.SUCCESS, 'Cadastro realizado com sucesso.')
        
        return redirect('pacientes')
    
def paciente_view(request, id):
    paciente = Pacientes.objects.get(id=id)
    if request.method == "GET":
        tarefas = Tarefas.objects.all()
        consultas = Consultas.objects.filter(paciente=paciente)
        total_consultas = consultas.count()
        
        tuple_grafico = ([str(i.data) for i in consultas], [str(i.humor) for i in consultas])
        
        return render(request, 'paciente.html', {'paciente' : paciente, 'tarefas' : tarefas, 'consultas' : consultas, 'tuple_grafico' : tuple_grafico, 'total_consultas' : total_consultas})
    elif request.method == "POST":
        humor = request.POST.get('humor')
        registro_geral = request.POST.get('registro_geral')
        video = request.FILES.get('video')
        tarefas = request.POST.getlist('tarefas')
        
        consultas = Consultas(
            humor = int(humor),
            registro_geral = registro_geral,
            video = video,
            paciente = paciente
        )
        
        consultas.save()
        
        for i in tarefas:
            tarefa = Tarefas.objects.get(id=i)
            consultas.tarefas.add(tarefa)
            
        consultas.save()
        
        messages.add_message(request, constants.SUCCESS, 'Registro adicionado com sucesso.')
        return redirect(f'/pacientes/{id}')
    
def atualizar_paciente(request, id):
    pagamento_em_dia = request.POST.get('pagamento_em_dia')
    paciente = Pacientes.objects.get(id=id)
    
    status = True if pagamento_em_dia == 'ativo' else False
    paciente.pagamento_em_dia = status
    paciente.save()
    
    return redirect(f'/pacientes/{id}')

def excluir_consulta(request,id):
    consulta = Consultas.objects.get(id=id)
    consulta.delete()
    return redirect(f'/pacientes/{consulta.paciente.id}')

def consulta_publica(request,id):
    consulta = Consultas.objects.get(id=id)
    if not consulta.paciente.pagamento_em_dia:
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
