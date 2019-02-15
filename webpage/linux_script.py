import paramiko
from .models import temp_linux_db
import os
import subprocess


def get_linux_ip():
	transport = paramiko.Transport(("13.233.43.190", 22))
	transport.connect(username = "ubuntu", password = "soe@123")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.get('/home/ubuntu/linux_list.txt','temp.txt')

	with open("temp.txt","r+") as file :
		strings = file.read()

	for string in strings.splitlines():
		try:
			if ':' in string:
				splitter_index = string.find(':')
				username = string[0:splitter_index-1]
				ip = string[splitter_index+2:]
				temp_linux_db.objects.create(host_name= username, host_ip = ip)
				# try:
				# 	ssh = paramiko.SSHClient()
				# 	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				# 	ssh.connect(ip,port=22, username=username, password="soe@123")
					
				# except:
				# 	pass
		except:
			pass

def linux_shutdown(username, ip):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port=22, username=username, password="soe@123",timeout=10)
	stdin, stdout, stderr = ssh.exec_command('sudo ls', get_pty = True)
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

