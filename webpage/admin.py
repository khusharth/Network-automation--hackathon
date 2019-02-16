from django.contrib import admin
from .models import  temp_linux_db,linux_software, playbook

admin.site.register(linux_software)
admin.site.register(temp_linux_db)
admin.site.register(playbook)

