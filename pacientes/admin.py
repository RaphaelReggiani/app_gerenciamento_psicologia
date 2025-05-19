from django.contrib import admin
from .models import Pacientes, Tarefas

# Register your models here.

admin.site.register(Pacientes)
admin.site.register(Tarefas)