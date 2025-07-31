from django import forms
from .models import Pacientes, Consultas
from .validators import name_validator, email_validator, phone_validator

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Pacientes
        fields = ['paciente_nome', 'paciente_email', 'paciente_telefone', 'paciente_queixa', 'paciente_foto']
    
    paciente_nome = forms.CharField(validators=[name_validator])
    paciente_email = forms.EmailField(validators=[email_validator])
    paciente_telefone = forms.CharField(validators=[phone_validator])


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consultas
        fields = ['paciente_humor', 'paciente_registro_geral', 'paciente_tarefa', 'paciente_frequencia', 'paciente_video']

    paciente_humor = forms.IntegerField(min_value=0, max_value=10)
    paciente_registro_geral = forms.CharField(widget=forms.Textarea, required=False)
    paciente_tarefa = forms.ChoiceField(choices=Consultas.tarefa_choices)
    paciente_frequencia = forms.ChoiceField(choices=Consultas.frequencia_choices)
    paciente_video = forms.FileField(required=False)
