from django.contrib import admin
from .models import  temp_linux_db,linux_software, temp_windows_db, windows_software

admin.site.register(linux_software)
admin.site.register(windows_software)
admin.site.register(temp_linux_db)
admin.site.register(temp_windows_db)


# Register your models here.
