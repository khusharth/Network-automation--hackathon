from crontab import CronTab
import sys

user=sys.argv[1]
cron = CronTab(user)  
job = cron.new(command='/usr/bin/python3 /bin/temp.py')  
job.minute.every(2)

cron.write()
