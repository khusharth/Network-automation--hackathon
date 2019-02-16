import paramiko
from .models import temp_linux_db, playbook
import os
import subprocess
import random
import time


def get_linux_ip():
	transport = paramiko.Transport(("13.233.162.29", 22))
	transport.connect(username = "ubuntu", password = "soe@123")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.get('/home/ubuntu/linux_list.txt','temp1.txt')

	with open("temp1.txt","r+") as file :
		strings = file.read()

	for string in strings.splitlines():
		try:
			if ':' in string:
				splitter_index = string.find(':')
				username = string[0:splitter_index-1]
				ip = string[splitter_index+2:]
				temp_linux_db.objects.create(host_name= username, host_ip = ip)
		except:
			pass

def linux_shutdown(username, ip):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port=22, username=username, password="soe@123",timeout=10)
	stdin, stdout, stderr = ssh.exec_command('sudo poweroff', get_pty = True)
	stdin.write('soe@123' + '\n')
	stdin.flush()
	print(stdout.readlines())
	print("Poweroff SEND")
			
def linux_runcommand(username, ip, command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port=22, username=username, password="soe@123", timeout=10)
	stdin, stdout, stderr = ssh.exec_command(command)
	return stdout.readlines()

def linux_runcommand_all(command):
	objects = temp_linux_db.objects.all()
	for obj in objects:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(obj.host_ip,port=22, username=obj.host_name, password="soe@123", timeout=10)
		stdin, stdout, stderr = ssh.exec_command(command)

def linux_upload_file(filename,filepath,hostname, hostip):
	os.system("sudo chmod +x "+filepath)
	transport = paramiko.Transport((hostip, 22))
	transport.connect(username = hostname, password = "soe@123")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.put(filepath,'/0x026f/Desktop/software/'+filename)
	sftp.close()
	transport.close()

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostip,port=22, username=hostname, password="soe@123",timeout=10)
	stdin, stdout, stderr = ssh.exec_command('sudo chmod +x /0x026f/Desktop/software/'+filename, get_pty = True)
	stdin.write('soe@123' + '\n')
	stdin.flush()

def linux_run_playbook(pk, hostip):
	os.system('touch inventory')
	with open("inventory","r+") as file :
		file.write("[game]\n")
		file.write(hostip)

	obj = playbook.objects.filter(pk=pk)
	for o in obj:
		yml_temp = o.playbook_content

	temp_file_name = "temp"+str(random.randint(0,26654))+".yml"
	os.system('touch tmp/'+temp_file_name)
	with open('tmp/'+temp_file_name,"r+") as file :
		file.write(yml_temp)

	os.system('ansible-playbook -i inventory tmp/'+temp_file_name)
	


def linux_run_playbook_all(pk):
	t_list = []
	transport = paramiko.Transport(("13.233.162.29", 22))
	transport.connect(username = "ubuntu", password = "soe@123")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.get('/home/ubuntu/linux_list.txt','tmp.txt')

	with open("tmp.txt","r+") as file :
		strings = file.read()

	text = ""
	for su in strings.splitlines():
		print(su)
		indexx = su.find(':')
		tr = su[indexx:]
		print(tr)
		t_list.append(tr)

	os.system('touch inventory')
	with open("inventory","r+") as file :

		file.write("[game]\n")
		file.write(text)

	obj = playbook.objects.filter(pk=pk)
	for o in obj:
		yml_temp = o.playbook_content


	temp_file_name = "temp"+str(random.randint(0,26654))+".yml"
	os.system('touch tmp/'+temp_file_name)
	with open("tmp/"+temp_file_name,"r+") as file :
		file.write(yml_temp)

	os.system('ansible-playbook -i inventory tmp/'+temp_file_name)
	

def delete_playbook(ip):
	playbook.objects.filter(pk=pk).delete()