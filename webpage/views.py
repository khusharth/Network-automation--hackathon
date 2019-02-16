from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage	
from .linux_script import get_linux_ip, linux_shutdown, linux_runcommand, linux_runcommand_all, linux_run_playbook, delete_playbook,linux_run_playbook_all
from .models import temp_linux_db,linux_software, playbook
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
				return HttpResponseRedirect('/linux')
		else:
			content = {
			'error' : "Provide Valid Credentials !!",
			}
			return render(request, 'registration/login.html', content)
	return render(request,'registration/login.html')


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
def linux_command(request, hostname, hostip):
	
	stdout = ""
	context = {
	'stdout':stdout,
	'command_ip':hostip,
	'command_hostname':hostname,
	}

	return render(request, 'webpage/linux_command.html', context)

@login_required(login_url="/")
def linux_command_all(request):
	if request.method == 'POST':
		if 'command_word' in request.POST:	
			command = request.POST['command_word']
			linux_runcommand_all(command)
	return render(request, 'webpage/linux_command_all.html')


@login_required(login_url="/")
def temp_linux_command(request):
	stdout = ""
	if request.method =="POST":
		
		stdout = linux_runcommand(request.POST['command_hostname'],request.POST['command_ip'], request.POST['command_word'][4:])
	print(stdout)

	context = {'stdout':stdout}

	command_form = render_to_string('webpage/temp_command.html',
		context,
		request=request,
		)
	return JsonResponse({'command_form':command_form})

def linux_playbook_all(request):
	return render(request, 'webpage/linux_command_all.html')


def linux_playbook(request, hostname, hostip):

	objects = playbook.objects.all()

	context = {
	'host_ip' : hostname,
	'host_name' : hostip,
	'objects':objects,
	}
	return render(request, 'webpage/linux_playbook.html', context)

def add_playbook(request):
	if request.method == 'POST':
		if 'playbook_head' in request.POST:
			playbook.objects.create(playbook_name= request.POST['playbook_head'], playbook_content = request.POST['playbook_content'])
			return HttpResponseRedirect('/linux')

	return render(request, 'webpage/add_playbook.html')

def edit_playbook(request, id):
	if request.method == 'POST':
		if 'playbook_head' in request.POST:
			playbook.objects.filter(pk=id).update(playbook_name= request.POST['playbook_head'], playbook_content = request.POST['playbook_content'])
			return HttpResponseRedirect('/linux')
	objects = playbook.objects.filter(pk=id)
	context = {
	'objects':objects,
	}
	return render(request, 'webpage/edit_playbook.html', context)

def run_playbook(request, id, hostip):
	linux_run_playbook_all(id)
	return HttpResponseRedirect('/linux')

def delete_playbook(request, ip):
	linux_delete_playbook(ip)
	return HttpResponseRedirect('/linux')
