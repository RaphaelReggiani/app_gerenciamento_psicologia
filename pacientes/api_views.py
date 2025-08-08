from rest_framework import viewsets
from .models import NewUser, Pacientes, Consultas, Visualizacoes
from .serializers import PacientesSerializer, ConsultasSerializer, VisualizacoesSerializer, NewUserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

class PacientesViewSet(viewsets.ModelViewSet):
    queryset = Pacientes.objects.all().order_by('-id')
    serializer_class = PacientesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ConsultasViewSet(viewsets.ModelViewSet):
    queryset = Consultas.objects.all().order_by('-paciente_data')
    serializer_class = ConsultasSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VisualizacoesViewSet(viewsets.ModelViewSet):
    queryset = Visualizacoes.objects.all()
    serializer_class = VisualizacoesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class NewUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewUser.objects.all().order_by('user_psicologo_nome')
    serializer_class = NewUserSerializer
    permission_classes = [AllowAny]