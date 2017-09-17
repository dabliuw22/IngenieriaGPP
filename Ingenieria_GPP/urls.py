"""Ingenieria_GPP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from apps.bienes.views import Index

urlpatterns = [
	url(r'^$', Index.as_view(), name = 'index'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('apps.bienes.urls', namespace = 'bien')),
    url(r'^', include('apps.locaciones.urls', namespace = 'locacion')),
    url(r'^accounts/login/$', login, {'template_name': 'usuario/usuario_login.html'}, name = 'login'),
    url(r'^logout/$', logout, name = 'logout'),
    url(r'^reset/password_reset$', password_reset, {'template_name': 'usuario/password/password_reset_form.html', 'email_template_name': 'usuario/password/password_reset_email.html'}, name='password_reset'),
    url(r'^reset/password_reset_done$', password_reset_done, {'template_name': 'usuario/password/password_reset_done.html'}, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name': 'usuario/password/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^reset/done$', password_reset_complete, {'template_name':'usuario/password/password_reset_complete.html'}, name='password_reset_complete')
]
if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

# Añadir
admin.site.site_header = 'Ingeniería GPP'