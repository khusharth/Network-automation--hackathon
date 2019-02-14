from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	path('home',views.home, name = 'home'),
	path('',views.home_login, name = 'home_login'),
	path('linux',views.linux, name = 'linux'),
	path('windows',views.windows, name = 'windows'),
	path('linux/command/<str:hostname>/<str:hostip>', views.linux_command, name='linux_command'),
	path('windows/command/<str:hostname>/<str:hostip>', views.windows_command, name='windows_command'),
	path('linux/command/execute/', views.temp_linux_command, name='temp_linux_command'),
	path('windows/command/execute/', views.temp_windows_command, name='temp_windows_command'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)