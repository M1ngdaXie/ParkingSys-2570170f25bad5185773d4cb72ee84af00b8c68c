from django.contrib import admin

# Register your models here.
from .models import Driver

class DriverAdmin(admin.ModelAdmin):
    pass 

admin.site.register(Driver)