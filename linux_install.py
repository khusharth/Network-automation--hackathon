import time
# time.sleep(100)

import socket
import subprocess
import getpass
import paramiko


#with open("/0x026f/Desktop/hackathone/error.txt","w") as file :
#    file.write("Error occured")

def func():
	ip = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
	username = getpass.getuser()
	transport = paramiko.Transport(("13.233.43.190", 22))
	transport.connect(username = "ubuntu", password = "soe@123")
	sftp = paramiko.SFTPClient.from_transport(transport)
	sftp.get('/home/ubuntu/linux_list.txt','temp.txt')
	with open("temp.txt","r+") as file :
		string = file.read()


	for s in string.splitlines():
		if username in s:
			if s[len(username)+3:] != ip:
				string = string.replace(s, username+' : '+ip)

	if username not in string:
		string = "\n"+string  + username +" : "+ ip 

	with open("temp.txt","w") as file :
		file.write(string.strip())

	sftp.put('temp.txt', '/home/ubuntu/linux_list.txt')

	sftp.close()
	transport.close()
func()
