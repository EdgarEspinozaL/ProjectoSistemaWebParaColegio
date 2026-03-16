from django.contrib import admin
from .models import RegistrosDiarios, Tarea

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )


# Register your models here.
admin.site.register(RegistrosDiarios, TaskAdmin)
admin.site.register(Tarea)