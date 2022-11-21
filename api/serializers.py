from rest_framework import serializers
from .models import *

class EstudiantesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiantes
        fields = '__all__'