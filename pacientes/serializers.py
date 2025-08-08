from rest_framework import serializers
from .models import Pacientes, Consultas, Visualizacoes , NewUser

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacientes
        fields = '__all__'

class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields = '__all__'

class VisualizacoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualizacoes
        fields = '__all__'

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        exclude = ['user_psicologo_password', 'reset_token']