from django.db import models

class Estudiantes(models.Model):
    id_estudiante = models.AutoField(primary_key=True)

    nombre = models.CharField(max_length=50, default='')
    apellidos = models.CharField(max_length=50, default='')

    n_control = models.CharField(max_length=10, default='')
    carrera = models.CharField(max_length=50, default='')
    campus = models.CharField(max_length=50, default='')

    ultimo_log = models.DateTimeField(auto_now=True)

    rfid = models.CharField(max_length=12, default='')

    telefono = models.CharField(max_length=10, default='')
    curp = models.CharField(max_length=18, default='')
    t_sangre = models.CharField(max_length=3, default='')
    alergias = models.CharField(max_length=50, default='')

    remark = models.CharField(max_length=50, default='')

    foto = models.BinaryField(max_length=10_000, null=True)

class Logs(models.Model):
    id_log = models.AutoField(primary_key=True)
    id_estudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE)

    tipo = models.CharField(max_length=50, default='')
    
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    dia_semana = models.CharField(max_length=50, default='')

    remark = models.CharField(max_length=50, default='')

# examlpe json for Estudiantes
# {
#     "id_estudiante": 1,
#     "nombre": "Diego",
#     "apellidos": "Garcia",
#     "n_control": "123456",
#     "carrera": "Ing. en Sistemas Computacionales",
#     "campus": "Tec de Monterrey Campus Puebla",
#     "rfid": "123456789012",
#     "telefono": "2222222222",
#     "curp": "GADG980101HDFRDF01",
#     "t_sangre": "O+",
#     "alergias": "Ninguna",
#     "remark": "Ninguna",
#     "foto": "base64"
# }

# examlpe json for Logs
# {
#     "id_estudiante": 1,
#     "tipo": "Entrada",
#     "dia_semana": "Lunes",
#     "remark": "Ninguna"
# }