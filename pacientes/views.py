from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Pacientes, Consultas, Visualizacoes, NewUser
from django.contrib import messages
from .forms import PacienteForm, ConsultaForm, SignUpForm, FinalizeUserForm, LoginForm, UserEditForm, PacienteEditForm
from django.contrib.messages import constants, get_messages
from django.db.models import Q
from django.core.exceptions import ValidationError
import re, secrets, datetime
from collections import Counter
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils.http import urlencode
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def user_auth(request):

    signup_form = SignUpForm(prefix='signup')
    login_form = LoginForm(prefix='login')
    return render(request, 'user.html', {
        'signup_form': signup_form,
        'login_form': login_form,
        'user_paises': NewUser.user_pais_choices,
        'user_dias': NewUser.user_dia_choices,
        'user_meses': NewUser.user_mes_choices,
        'user_anos': NewUser.user_ano_choices,
    })

def user_pre_register(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            cleaned_data = signup_form.cleaned_data

            request.session['pre_user_data'] = {
                'user_psicologo_nome': cleaned_data['user_psicologo_nome'],
                'user_psicologo_email': cleaned_data['user_psicologo_email'],
                'user_psicologo_telefone': cleaned_data['user_psicologo_telefone'],
                'user_psicologo_pais': cleaned_data['user_psicologo_pais'],
                'user_psicologo_dia': cleaned_data['user_psicologo_dia'],
                'user_psicologo_mes': cleaned_data['user_psicologo_mes'],
                'user_psicologo_ano': cleaned_data['user_psicologo_ano'],
            }

            return redirect('user_finalize_register')
        else:
            messages.error(request, 'Por favor, corrija os campos abaixo.')
            login_form = LoginForm(prefix='login')
            return render(request, 'user.html', {
                'signup_form': signup_form,
                'login_form': login_form,
                'user_paises': NewUser.user_pais_choices,
                'user_dias': NewUser.user_dia_choices,
                'user_meses': NewUser.user_mes_choices,
                'user_anos': NewUser.user_ano_choices,
            })
    return redirect('user')

def user_finalize_register(request):
    pre_user_data = request.session.get('pre_user_data')
    if not pre_user_data:
        messages.error(request, "Por favor, complete a primeira etapa para finalizar o registro.")
        return redirect('user')
    
    success = False

    if request.method == 'POST':
        form = FinalizeUserForm(request.POST)
        if form.is_valid():
            user_psicologo_nickname = form.cleaned_data['user_psicologo_nickname']

            if NewUser.objects.filter(user_psicologo_nickname=user_psicologo_nickname).exists():
                messages.error(request, 'Este nome de usuário já existe.')
            else:

                user = NewUser(
                    user_psicologo_nome=pre_user_data['user_psicologo_nome'],
                    user_psicologo_email=pre_user_data['user_psicologo_email'],
                    user_psicologo_telefone=pre_user_data['user_psicologo_telefone'],
                    user_psicologo_pais=pre_user_data['user_psicologo_pais'],
                    user_psicologo_dia=pre_user_data['user_psicologo_dia'],
                    user_psicologo_mes=pre_user_data['user_psicologo_mes'],
                    user_psicologo_ano=pre_user_data['user_psicologo_ano'],
                    user_psicologo_nickname=user_psicologo_nickname,
                    user_psicologo_password=make_password(form.cleaned_data['user_psicologo_password']),
                )
                user.save()

                del request.session['pre_user_data']

                messages.success(request, 'Usuário registrado com sucesso.')
                success = True
        else:
            messages.error(request, 'Este nome de usuário já existe, escolha outro.')
    else:
        form = FinalizeUserForm()

    return render(request, 'user_register.html', {'form': form, 'success': success})

def user_login(request):
    if request.method == 'POST':
        user_psicologo_nickname = request.POST.get('user_psicologo_nickname')
        user_psicologo_password = request.POST.get('user_psicologo_password')
        user_psicologo_nome = request.POST.get('user_psicologo_nome')

        try:
            user = NewUser.objects.get(user_psicologo_nickname=user_psicologo_nickname)
            if check_password(user_psicologo_password, user.user_psicologo_password):

                request.session['user_id'] = user.id
                request.session['user_psicologo_nickname'] = user.user_psicologo_nickname
                request.session['user_psicologo_nome'] = user.user_psicologo_nome

                messages.success(request, f'Bem vindo(a), {user.user_psicologo_nome}!', extra_tags='login')
                return redirect('home')
            else:
                messages.error(request, 'Senha incorreta.', extra_tags='login')
        except NewUser.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.', extra_tags='login')

    signup_form = SignUpForm(prefix='signup')
    login_form = LoginForm(prefix='login')
    return render(request, 'user.html', {
        'signup_form': signup_form,
        'login_form': login_form,
        'user_paises': NewUser.user_pais_choices,
        'user_dias': NewUser.user_dia_choices,
        'user_meses': NewUser.user_mes_choices,
        'user_anos': NewUser.user_ano_choices,
    })

def user_logout(request):

    request.session.flush()
    storage = get_messages(request)

    for _ in storage:
        pass

    return redirect('home')

def user_informations(request, user_id):
    session_user_id = request.session.get('user_id')
    if not session_user_id:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("user_login")

    if int(session_user_id) != int(user_id):
        messages.error(request, "Você não tem acesso a este usuário.")
        return redirect("home")

    try:
        user = NewUser.objects.get(id=session_user_id)
    except NewUser.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("home")

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Suas informações foram atualizadas.")
            return redirect('user_informations', user_id=user.id)
        else:
            messages.error(request, "Ocorreu um erro com o formulário.")
    else:
        form = UserEditForm(instance=user)

    return render(request, 'user_informations.html', {
        'user': user,
        'form': form,
        'user_paises': NewUser.user_pais_choices,
        'user_dias': NewUser.user_dia_choices,
        'user_meses': NewUser.user_mes_choices,
        'user_anos': NewUser.user_ano_choices,
    })

def user_forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = NewUser.objects.get(user_psicologo_email=email)

            token = secrets.token_urlsafe(32)
            user.reset_token = token
            user.save()

            reset_link = request.build_absolute_uri(
                f"/user/reset-password/?{urlencode({'token': token})}"
            )

            send_mail(
                'Password Reset - App Psicologia',
                f'Olá {user.user_psicologo_nickname},\n\nClique no link abaixo para recuperar a senha:\n{reset_link}',
                'noreply@apsicologia.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, "As instruções de recuperação de senha foram enviadas para o e-mail cadastrado.")
            return redirect('user_login')

        except NewUser.DoesNotExist:
            messages.error(request, "Usuário não encontrado.")

    return render(request, 'user_forgot_password.html')

def user_reset_password(request):
    token = request.GET.get('token')
    if not token:
        messages.error(request, "Token inválido.")
        return redirect("user_login")

    try:
        user = NewUser.objects.get(reset_token=token)
    except NewUser.DoesNotExist:
        messages.error(request, "Token inválido ou expirado.")
        return redirect("user_login")

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "As senhas precisam ser iguais.")
        else:
            user.user_psicologo_password = make_password(new_password)
            user.reset_token = ''
            user.save()
            messages.success(request, "Senha atualizada.")
            return redirect("user_login")

    return render(request, 'user_reset_password.html')

def pacientes(request):

    user_id = request.session.get('user_id')

    if request.method == "POST":
        form = PacienteForm(request.POST, request.FILES)
        
        if form.is_valid():

            if not user_id:
                messages.error(request, "Você precisa estar logado para cadastrar um paciente.")
                return redirect('pacientes')
            
            paciente_nome = form.cleaned_data['paciente_nome']
            paciente_email = form.cleaned_data['paciente_email']
            paciente_telefone = form.cleaned_data['paciente_telefone']
            
            paciente_existente = Pacientes.objects.filter(
                Q(paciente_nome=paciente_nome) |
                Q(paciente_email=paciente_email) |
                Q(paciente_telefone=paciente_telefone),
                paciente_ref_psicologo_id=user_id
            ).first()

            if paciente_existente:
                messages.error(request, 'Nome, e-mail ou telefone já cadastrados.')
                return redirect('pacientes')
            
            paciente = form.save(commit=False)
            paciente.paciente_ref_psicologo_id = user_id
            paciente.save()
            messages.success(request, "Paciente cadastrado com sucesso.")
            return redirect('pacientes')
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)
            return redirect('pacientes')

    else:
        form = PacienteForm()
        pacientes = Pacientes.objects.filter(paciente_ref_psicologo_id=user_id)
        show_pacientes = pacientes.order_by('-id')
        return render(request, 'pacientes.html', {
            'form': form,
            'paciente_queixas': Pacientes.queixa_choices, 
            'paciente_dias': Pacientes.paciente_dia_choices,
            'paciente_meses': Pacientes.paciente_mes_choices,
            'paciente_anos': Pacientes.paciente_ano_choices,
            'paciente_paises': Pacientes.paciente_pais_choices,
            'pacientes': pacientes, 
            'show_pacientes': show_pacientes,
        })
    
def paciente_registro(request, id):
    paciente = Pacientes.objects.get(id=id)
    user_id = request.session.get('user_id')
    psicologo_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect('user_login')

    if paciente.paciente_ref_psicologo_id != user_id:
        messages.error(request, "Você não tem permissão para acessar este paciente.")
        return redirect('home')

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
            'psicologo_id': psicologo_id,
        })

    elif request.method == "POST":
        form = ConsultaForm(request.POST, request.FILES)

        if form.is_valid() and paciente.paciente_pagamento_em_dia == True:
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
            if paciente.paciente_pagamento_em_dia == False:
                messages.error(request, 'Usuário Inativo. Não foi possível realizar o registro.')
            else:
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
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Você precisa estar logado para atualizar o paciente.")
        return redirect('user_login')

    paciente = Pacientes.objects.get(id=id)

    if paciente.paciente_ref_psicologo_id != user_id:
        messages.error(request, "Você não tem permissão para atualizar este paciente.")
        return redirect('home')

    paciente_pagamento_em_dia = request.POST.get('paciente_pagamento_em_dia')
    status = paciente_pagamento_em_dia == 'ativo'
    paciente.paciente_pagamento_em_dia = status
    paciente.save()

    messages.success(request, "Status de pagamento atualizado com sucesso.")
    return redirect(f'/pacientes/{id}')


def excluir_consulta(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Você precisa estar logado para excluir uma consulta.")
        return redirect('user_login')

    try:
        consulta = Consultas.objects.get(id=id)
    except Consultas.DoesNotExist:
        messages.error(request, "Consulta não encontrada.")
        return redirect('home')

    if consulta.paciente.paciente_ref_psicologo_id != user_id:
        messages.error(request, "Você não tem permissão para excluir esta consulta.")
        return redirect('home')

    consulta.delete()
    messages.success(request, "Consulta excluída com sucesso.")
    return redirect(f'/pacientes/{consulta.paciente.id}')

def consulta_publica(request, id):
    try:
        consulta = Consultas.objects.get(id=id)
    except Consultas.DoesNotExist:
        raise Http404("Consulta não encontrada.")

    Visualizacoes.objects.create(
        consulta=consulta,
        ip=request.META.get('REMOTE_ADDR', '0.0.0.0')
    )

    return render(request, 'consulta_publica.html', {'consulta': consulta})

def excluir_paciente(request, id):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, "Você precisa estar logado para excluir um paciente.")
        return redirect('user_login')

    paciente = get_object_or_404(Pacientes, id=id)

    if paciente.paciente_ref_psicologo_id != user_id:
        messages.error(request, "Você não tem permissão para excluir este paciente.")
        return redirect('pacientes')

    paciente.delete()
    messages.success(request, "Paciente excluído com sucesso.")
    return redirect('pacientes')

def user_psicologo_pacientes(request, user_id):
    session_user_id = request.session.get('user_id')
    if not session_user_id or session_user_id != user_id:
        messages.error(request, "Você precisa estar logado para acessar esta página.")
        return redirect("user_login")

    try:
        user = NewUser.objects.get(id=session_user_id)
    except NewUser.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect("home")

    query = request.GET.get('q', '')
    queixa = request.GET.get('queixa', '')

    queixas_choices = Pacientes.queixa_choices

    pacientes = Pacientes.objects.filter(paciente_ref_psicologo=user)

    if query:
        pacientes = pacientes.filter(
            Q(paciente_nome__icontains=query) |
            Q(paciente_queixa__icontains=query)
        )

    if queixa:
        pacientes = pacientes.filter(paciente_queixa=queixa)

    pacientes = pacientes.distinct().order_by('-id')

    return render(request, 'user_psicologo_pacientes.html', {
        'pacientes': pacientes,
        'query': query,
        'queixas_choices': queixas_choices,
    })

def paciente_edit(request, id):
    try:
        paciente = Pacientes.objects.get(id=id)
    except Pacientes.DoesNotExist:
        raise Http404("Paciente não encontrado.")
    
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("user")

    if paciente.paciente_ref_psicologo.id != user_id:
        messages.error(request, "Você não tem permissão para editar este paciente.")
        return redirect("user_psicologo_pacientes", user_id=user_id)

    if request.method == "GET":
        return render(request, 'paciente_edit.html', {
            'paciente_queixas': Pacientes.queixa_choices, 
            'paciente_dias': Pacientes.paciente_dia_choices,
            'paciente_meses': Pacientes.paciente_mes_choices,
            'paciente_anos': Pacientes.paciente_ano_choices,
            'paciente_paises': Pacientes.paciente_pais_choices,
            'paciente' : paciente,
        })

    elif request.method == "POST":
        form = PacienteEditForm(request.POST, request.FILES, instance=paciente)

        if form.is_valid():
            form.save()
            messages.success(request, "Informações atualizadas com sucesso.")
            return redirect('paciente_edit', id=id)
        else:
            messages.error(request, "Erro ao atualizar o paciente. Insira os dados corretos.")
            return render(request, 'paciente_edit.html', {
                'paciente_queixas': Pacientes.queixa_choices, 
                'paciente_dias': Pacientes.paciente_dia_choices,
                'paciente_meses': Pacientes.paciente_mes_choices,
                'paciente_anos': Pacientes.paciente_ano_choices,
                'paciente_paises': Pacientes.paciente_pais_choices,
                'paciente' : paciente,
                'form_errors': form.errors,
            })