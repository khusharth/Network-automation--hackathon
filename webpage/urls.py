from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('home',views.home, name = 'home'),
    path('',views.home_login, name = 'home_login'),
    path('upload_software',views.upload_software, name = 'upload_software'),
    path('install_software',views.install_software, name = 'install_software'),
    path('install_software_linux',views.install_software_linux, name = 'install_software_linux'),
    path('linux/command', views.install_software_linux_command, name='linux_command')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)