import paramiko
from .models import temp_windows_db
import os


def get_windows_ip():
	transport = paramiko.Transport(("13.233.43.190", 22))
	transport.connect(username = "ubuntu", password = "soe@123")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.get('/home/ubuntu/windows_list.txt','temp1.txt')

	with open("temp1.txt","r+") as file :
		strings = file.read()

	for string in strings.splitlines():
		try:
			# print(string)
			if ':' in string:
				splitter_index = string.find(':')
				username = string[0:splitter_index-1]
				ip = string[splitter_index+2:]
				temp_windows_db.objects.create(host_name= username, host_ip = ip)
		except:
			pass

def windows_upload_file(filename, filepath, hostname, hostip):
	os.system("sudo chmod +x "+filepath)

	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostip,port=22, username=hostname, password="0x026f!@",timeout=10)
	stdin, stdout, stderr = ssh.exec_command('mkdir C:\\software\\')

	transport = paramiko.Transport((hostip, 22))
	transport.connect(username = hostname, password = "0x026f!@")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.put(filepath,'C:\\software\\'+filename)
	sftp.close()
	transport.close()

def windows_runcommand(username, ip, command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port=22, username=username, password="0x026f!@", timeout=10)
	stdin, stdout, stderr = ssh.exec_command(command)
	return stdout.readlines()
