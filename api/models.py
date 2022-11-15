from django.db import models

class Estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)

    n_control = models.CharField(max_length=10)
    carrera = models.CharField(max_length=50)
    campus = models.CharField(max_length=50)

    telefono = models.CharField(max_length=10)
    curp = models.CharField(max_length=18)
    t_sangre = models.CharField(max_length=3)
    alergias = models.CharField(max_length=50)

    remark = models.CharField(max_length=50)

    foto = models.BinaryField(max_length=10_000)
    