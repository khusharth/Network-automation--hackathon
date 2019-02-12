import paramiko
import os
import socket    
import multiprocessing
import subprocess
import os
from .models import temp_linux_db


def pinger(job_q, results_q):
	temp_ip_list = []
	DEVNULL = open(os.devnull, 'w')
	while True:

		ip = job_q.get()

		if ip is None:
			break

		try:
			subprocess.check_call(['ping', '-c1', ip],stdout=DEVNULL)
			
			results_q.put(ip)
			temp_ip_list.append(ip)
						
		except:
			pass

def get_my_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return ip


def map_network(pool_size=255):

	ip_list = list()

	ip_parts = get_my_ip().split('.')
	base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'

	jobs = multiprocessing.Queue()
	results = multiprocessing.Queue()
	os_list = multiprocessing.Queue()

	pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

	for p in pool:
		p.start()

	for i in range(1, 255):
		jobs.put(base_ip + '{0}'.format(i))

	for p in pool:
		jobs.put(None)

	for p in pool:
		p.join()

	while not results.empty():
		ip = results.get()
		ip_list.append(ip)

	return ip_list

def get_os(ip_list):
	linux_ip_list = []
	linux_results = multiprocessing.Queue()
	print(ip_list)
	pool = [multiprocessing.Process(target=linux_checker, args=(ip, linux_results)) for ip in ip_list]

	for p in pool:
		p.start()

	for p in pool:
		p.join()

	while not linux_results.empty():
		ip = linux_results.get()
		linux_ip_list.append(ip)

	return linux_ip_list

def linux_checker(ip, linux_results):
	temp_ip_list = []
	DEVNULL = open(os.devnull, 'w')
	try:
		print(ip)
		temp = subprocess.check_output(['nmap', '-O', ip], timeout=10)
		if 'linux' in str(temp):
			print("IP : " + ip)
			print("OS : Linux" )
			linux_results.put(ip)
		elif 'host' in str(temp):
			print("IP : " + ip)
			print("OS : Unknown" )
					
	except:
		pass


def get_linux_ip():
	active_ip = map_network()
	print(active_ip)
	linux_ips = get_os(active_ip)

	for ip in linux_ips:
		try:
			print(ip)
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(ip,port=22, username="root", password="soe@123", timeout=10)
			stdin, stdout, stderr = ssh.exec_command('getent passwd | cut -d : -f 1 | xargs groups | grep "sudo"')
			username = stdout.readlines()[0].split()[0]

			if not (username is None):
				print("Found \nIP : " + ip +"\nUsername : "+ username)
				temp = temp_linux_db.objects.create(host_name= username, host_ip = ip)			

			if username is None:
				print("Not Found")
			
		except:
			pass

def linux_shutdown(ip):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port=22, username="root", password="soe@123",timeout=10)
	stdin, stdout, stderr = ssh.exec_command('poweroff')
	print("Poweroff SEND")
	
			
def linux_runcommand(ip, command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip,port=22, username="root", password="soe@123", timeout=10)
	stdin, stdout, stderr = ssh.exec_command(command)
	return stdout.readlines()