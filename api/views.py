from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .models import Estudiantes
from .serializers import EstudiantesSerializer


# Create your views here.

@csrf_exempt
def estudiantes_list(request):
    if request.method == 'GET':
        estudiantes = Estudiantes.objects.all()
        estudiantes_serializer = EstudiantesSerializer(estudiantes, many=True)
        return JsonResponse(estudiantes_serializer.data, safe=False)

    elif request.method == 'POST':
        estudiantes_data = JSONParser().parse(request)
        estudiantes_serializer = EstudiantesSerializer(data=estudiantes_data)
        if estudiantes_serializer.is_valid():
            estudiantes_serializer.save()
            return JsonResponse(estudiantes_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(estudiantes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
def estudiantes_detail(request, pk):
    try:
        estudiantes = Estudiantes.objects.get(pk=pk)
    except Estudiantes.DoesNotExist:
        return JsonResponse({'message': 'The Estudiante does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        estudiantes_serializer = EstudiantesSerializer(estudiantes)
        return JsonResponse(estudiantes_serializer.data)

    elif request.method == 'PUT':
        estudiantes_data = JSONParser().parse(request)
        estudiantes_serializer = EstudiantesSerializer(estudiantes, data=estudiantes_data)
        if estudiantes_serializer.is_valid():
            estudiantes_serializer.save()
            return JsonResponse(estudiantes_serializer.data)
        return JsonResponse(estudiantes_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        estudiantes.delete()
        return JsonResponse({'message': 'Estudiante was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

