import paramiko
import subprocess


transport = paramiko.Transport(("13.233.162.29", 22))
transport.connect(username = "ubuntu", password = "soe@123")
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.get('/home/ubuntu/linux_install.py','/bin/temp.py')

