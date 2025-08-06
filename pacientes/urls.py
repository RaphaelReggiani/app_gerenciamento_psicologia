from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user/', views.user_auth, name="user"),
    path('user/pre-register/', views.user_pre_register, name="user_pre_register"),
    path('user/finalize/', views.user_finalize_register, name="user_finalize_register"),
    path('user/login/', views.user_login, name='user_login'),
    path('user/logout/', views.user_logout, name='user_logout'),
    path('user/informations/<int:user_id>', views.user_informations, name="user_informations"),
    path('user/forgot-password/', views.user_forgot_password, name='user_forgot_password'),
    path('user/reset-password/', views.user_reset_password, name='user_reset_password'),
    path('user/user_psicologo_pacientes/<int:user_id>', views.user_psicologo_pacientes, name="user_psicologo_pacientes"),
    path('pacientes/', views.pacientes, name="pacientes"),
    path('<int:id>', views.paciente_registro, name="paciente_registro"),
    path('atualizar_paciente/<int:id>', views.atualizar_paciente, name="atualizar_paciente"),
    path('excluir_consulta/<int:id>', views.excluir_consulta, name="excluir_consulta"),
    path('consulta_publica/<int:id>', views.consulta_publica, name="consulta_publica"),
    path('excluir_paciente/<int:id>', views.excluir_paciente, name="excluir_paciente"),
    path('paciente_edit/<int:id>', views.paciente_edit, name="paciente_edit"),
]