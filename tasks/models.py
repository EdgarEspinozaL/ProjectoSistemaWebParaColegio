from django.db import models
from django.contrib.auth.models import User

# modelo de datos para los registros diarios.
class RegistrosDiarios(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stress_level = models.PositiveSmallIntegerField(default=0) 

    def __str__(self):
        return self.title + '- by' + self.user.username
    

# Modelo de datos para las tareas.
class Tarea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha = models.DateField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo