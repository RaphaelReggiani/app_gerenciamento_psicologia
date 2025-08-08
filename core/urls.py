from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pacientes import views as pacientes_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pacientes_views.home, name='home'),
    path('pacientes/', include('pacientes.urls')),
    path('api/', include('pacientes.api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
