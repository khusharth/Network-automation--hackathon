from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
	# path('home',views.home, name = 'home'),
	path('',views.home_login, name = 'home_login'),
	path('linux',views.linux, name = 'linux'),
	# path('windows',views.windows, name = 'windows'),
	path('linux/command/<str:hostname>/<str:hostip>', views.linux_command, name='linux_command'),
	# path('windows/command/<str:hostname>/<str:hostip>', views.windows_command, name='windows_command'),
	path('linux/command/execute/', views.temp_linux_command, name='temp_linux_command'),
	# path('windows/command/execute/', views.temp_windows_command, name='temp_windows_command'),
	path('linux/command/linux_all/', views.linux_command_all, name='linux_command_all'),
	# path('windows/command/windows_all/', views.windows_command_all, name='windows_command_all'),
	path('linux/playbook/linux_all/', views.linux_playbook_all, name='linux_playbook_all'),
	path('linux/playbook/<str:hostname>/<str:hostip>', views.linux_playbook, name='linux_playbook'),
	path('playbook/add', views.add_playbook, name='add_playbook'),
	path('playbook/edit/<int:id>', views.edit_playbook, name='edit_playbook'),
	path('playbook/run/<int:id>/<str:hostip>', views.run_playbook, name='run_playbook'),
	path('playbook/delete/<int:id>/', views.delete_playbook, name='delete_playbook'),
	
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)