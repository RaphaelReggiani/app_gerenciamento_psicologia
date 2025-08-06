from django import forms
from .models import Pacientes, Consultas, NewUser
from .validators import name_validator, email_validator, phone_validator
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = [
            'user_psicologo_nome', 
            'user_psicologo_email', 
            'user_psicologo_telefone', 
            'user_psicologo_dia', 
            'user_psicologo_mes', 
            'user_psicologo_ano', 
            'user_psicologo_pais',
        ]


class FinalizeUserForm(forms.ModelForm):
    user_psicologo_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text="A senha deve conter entra 6 e 12 caracteres (1 número e 1 caracter especial)."
    )

    class Meta:
        model = NewUser
        fields = [
            'user_psicologo_nickname', 
            'user_psicologo_password',
        ]

    def clean_user_nickname(self):
        nickname = self.cleaned_data.get('user_psicologo_nickname')
        if NewUser.objects.exclude(id=self.instance.id).filter(user_psicologo_nickname=nickname).exists():
            raise ValidationError("Este nome de usuário já existe.")
        return nickname

    def clean_user_password(self):
        password = self.cleaned_data.get('user_psicologo_password')

        if len(password) < 6 or len(password) > 10:
            raise ValidationError("A senha deve ter entre 6 e 12 caracteres.")

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_psicologo_password = self.cleaned_data['user_psicologo_password']
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    user_psicologo_nickname = forms.CharField(max_length=15, required=True)
    user_psicologo_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        nickname = cleaned_data.get("user_psicologo_nickname")
        password = cleaned_data.get("user_psicologo_password")

        if nickname and password:
            try:
                user = NewUser.objects.get(user_psicologo_nickname=nickname)
                if user.user_psicologo_password != password:
                    raise ValidationError("Senha incorreta.")
            except NewUser.DoesNotExist:
                raise ValidationError("Este usuário não existe.")
        return cleaned_data
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = NewUser
        fields = [
            'user_psicologo_nome',
            'user_psicologo_email',
            'user_psicologo_telefone',
            'user_psicologo_pais',
            'user_psicologo_dia',
            'user_psicologo_mes',
            'user_psicologo_ano',
        ]

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = [
            'paciente_nome', 
            'paciente_email', 
            'paciente_telefone', 
            'paciente_queixa', 
            'paciente_foto',
            'paciente_dia',
            'paciente_mes',
            'paciente_ano',
            'paciente_pais',
        ]
    
    paciente_nome = forms.CharField(validators=[name_validator])
    paciente_email = forms.EmailField(validators=[email_validator])
    paciente_telefone = forms.CharField(validators=[phone_validator])

class PacienteEditForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = [
            'paciente_nome',
            'paciente_email',
            'paciente_telefone',
            'paciente_foto',
            'paciente_dia',
            'paciente_mes',
            'paciente_ano',
            'paciente_pais',
        ]

    paciente_nome = forms.CharField(validators=[name_validator])
    paciente_email = forms.EmailField(validators=[email_validator])
    paciente_telefone = forms.CharField(validators=[phone_validator])

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultas
        fields = [
            'paciente_humor', 
            'paciente_registro_geral', 
            'paciente_tarefa', 
            'paciente_frequencia', 
            'paciente_video',
        ]

    paciente_humor = forms.IntegerField(min_value=0, max_value=10)
    paciente_registro_geral = forms.CharField(widget=forms.Textarea, required=False)
    paciente_tarefa = forms.ChoiceField(choices=Consultas.tarefa_choices)
    paciente_frequencia = forms.ChoiceField(choices=Consultas.frequencia_choices)
    paciente_video = forms.FileField(required=False)
