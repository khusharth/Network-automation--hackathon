import os
import sys
user = sys.argv[1]

os.system("python3 run_linux.py")
os.system("python cronjob.py "+ user)
