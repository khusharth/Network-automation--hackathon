from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage	
from .linux_script import get_linux_ip, linux_shutdown, linux_runcommand, linux_upload_file
from .windows_script import get_windows_ip, windows_runcommand, windows_upload_file
from .models import temp_linux_db,linux_software, temp_windows_db, windows_software
from django.template.loader import render_to_string
from django.conf import settings


def home_login(request):
	content = []
	if request.POST:
		username = '0x026f'
		password = request.POST['password']
		user = authenticate(username=username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				if request.GET.get('next', None):
					return HttpResponseRedirect(request.GET['next'])
				return HttpResponseRedirect('/home')
		else:
			content = {
			'error' : "Provide Valid Credentials !!",
			}
			return render(request, 'registration/login.html', content)
	return render(request,'registration/login.html')


@login_required(login_url="/")
def home(request):
	return render(request,'webpage/index.html')


@login_required(login_url="/")
def linux(request):
	count = temp_linux_db.objects.all().count()
	if(count == 0):
		get_linux_ip()
		
	if request.POST:
		if 'shutdown' in request.POST:
			linux_shutdown(request.POST['shutdown_hostname'],request.POST['shutdown_ip'])

		if 'refresh' in request.POST:
			temp_linux_db.objects.all().delete()
			get_linux_ip()


	linux_ip = temp_linux_db.objects.all()
	content = {
	'linux_ip' : linux_ip,
	}

	return render(request, 'webpage/linux.html', content)

@login_required(login_url="/")
def windows(request):
	count = temp_windows_db.objects.all().count()
	if(count == 0):
		get_windows_ip()

	if request.POST:
		# if 'shutdown' in request.POST:
		# 	linux_shutdown(request.POST['shutdown_hostname'],request.POST['shutdown_ip'])

		if 'refresh' in request.POST:
			temp_windows_db.objects.all().delete()
			get_windows_ip()

	windows_ip = temp_windows_db.objects.all()
	for a in windows_ip:
		print(a)
	content = {
	'windows_ip' : windows_ip,
	}
	return render(request, 'webpage/windows.html', content)


def linux_command(request, hostname, hostip):
	stdout = ""
	if request.method == 'POST':
		if 'software_name' in request.POST:
			linux_software.objects.create(linux_software_name = request.POST['software_name'], linux_software_location=request.FILES['myfile'])
			filepath = settings.MEDIA_ROOT+"/software/"+request.FILES['myfile'].name
			linux_upload_file(request.FILES['myfile'].name,filepath, hostname, hostip)
	context = {
	'stdout':stdout,
	'command_ip':hostip,
	'command_hostname':hostname,
	}

	return render(request, 'webpage/linux_command.html', context)

def windows_command(request, hostname, hostip):
	stdout = ""
	if request.method == 'POST':
		if 'software_name' in request.POST:
			windows_software.objects.create(windows_software_name = request.POST['software_name'], windows_software_location=request.FILES['myfile'])
			filepath = settings.MEDIA_ROOT+"/software/"+request.FILES['myfile'].name
			print(filepath)
			windows_upload_file(request.FILES['myfile'].name,filepath, hostname, hostip)
	context = {
	'stdout':stdout,
	'command_ip':hostip,
	'command_hostname':hostname,
	}

	return render(request, 'webpage/windows_command.html', context)

def temp_linux_command(request):
	stdout = ""
	print(request.POST['command_word'][4:])
	print(request.POST['command_ip'])
	print(request.POST['command_hostname'])
	if request.method =="POST":
		
		stdout = linux_runcommand(request.POST['command_hostname'],request.POST['command_ip'], request.POST['command_word'][4:])
	print(stdout)

	context = {'stdout':stdout}

	command_form = render_to_string('webpage/temp_command.html',
		context,
		request=request,
		)
	return JsonResponse({'command_form':command_form})

def temp_windows_command(request):
	stdout = ""
	print(request.POST['command_word'][4:])
	print(request.POST['command_ip'])
	print(request.POST['command_hostname'])
	if request.method =="POST":
		
		stdout = windows_runcommand(request.POST['command_hostname'],request.POST['command_ip'], request.POST['command_word'][4:])
	print(stdout)

	context = {'stdout':stdout}

	command_form = render_to_string('webpage/temp_command.html',
		context,
		request=request,
		)
	return JsonResponse({'command_form':command_form})
