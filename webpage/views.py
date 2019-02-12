from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from .forms import upload_software_form
from .scripts import get_linux_ip, linux_shutdown, linux_runcommand
from .models import temp_linux_db
from django.template.loader import render_to_string


def home_login(request):
	content = []
	if request.POST:
		username = '0x026f'
		password = request.POST['password']
		user = authenticate(username=username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				temp_linux_db.objects.all().delete()
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
def upload_software(request):
	if request.method == 'POST':
		form = upload_software_form(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = upload_software_form()

	return render(request, 'webpage/upload_software.html',{
		'form':form,
		})

@login_required(login_url="/")
def install_software(request):
	return render(request, 'webpage/install_software.html')


@login_required(login_url="/")
def install_software_linux(request):
	count = temp_linux_db.objects.all().count()
	if(count == 0):
		get_linux_ip()
		
	if request.POST:
		if 'shutdown' in request.POST:
			linux_shutdown(request.POST['shutdown_ip'])

		if 'refresh' in request.POST:
			temp_linux_db.objects.all().delete()
			get_linux_ip()


	linux_ip = temp_linux_db.objects.all()
	content = {
	'linux_ip' : linux_ip,
	}

	return render(request, 'webpage/install_software_linux.html', content)

def install_software_linux_command(request):
	stdout = ""
	if request.method =="POST":
		stdout = linux_runcommand(request.POST['command_ip'], request.POST['command_word'][4:])
	print(stdout)
	context = {'stdout':stdout}

	command_form = render_to_string('webpage/temp_command_res.html',
		context,
		request=request,
		)
	return JsonResponse({'command_form':command_form})