import datetime
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from .models import *
from .serializers import *


# Create your views here.

@csrf_exempt
def estudiantes_list(request):
    if request.method == 'GET':
        estudiantes = Estudiantes.objects.all().order_by('-ultimo_log')[:500]
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

@csrf_exempt
def logs_list(request):
    if request.method == 'GET':
        # GET ONLY LAST 500 LOGS
        logs = Logs.objects.all().order_by('-id_log')[:500]
        logs_serializer = LogsSerializer(logs, many=True)
        return JsonResponse(logs_serializer.data, safe=False)

    elif request.method == 'POST':
        logs_data = JSONParser().parse(request)
        logs_serializer = LogsSerializer(data=logs_data)
        if logs_serializer.is_valid():
            logs_serializer.save()
            return JsonResponse(logs_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(logs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def logs_detail(request, pk):
    try:
        logs = Logs.objects.all().order_by('-id_log')[:500].get(pk=pk)
    except Logs.DoesNotExist:
        return JsonResponse({'message': 'The Log does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        logs_serializer = LogsSerializer(logs)
        return JsonResponse(logs_serializer.data)

    elif request.method == 'PUT':
        logs_data = JSONParser().parse(request)
        logs_serializer = LogsSerializer(logs, data=logs_data)
        if logs_serializer.is_valid():
            logs_serializer.save()
            return JsonResponse(logs_serializer.data)
        return JsonResponse(logs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        logs.delete()
        return JsonResponse({'message': 'Log was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def logs_estudiante(request, pk):
    try:
        logs = Logs.objects.filter(id_estudiante=pk).order_by('-id_log')[:500]
    except Logs.DoesNotExist:
        return JsonResponse({'message': 'The Log does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        logs_serializer = LogsSerializer(logs, many=True)
        return JsonResponse(logs_serializer.data, safe=False)

    elif request.method == 'POST':
        logs_data = JSONParser().parse(request)
        logs_data["id_estudiante"] = pk

        now_date = datetime.datetime.now()
        now_hour = now_date.strftime("%H:%M:%S")
        now_date = now_date.strftime("%Y-%m-%d")

        # GET NUMBER OF DAY OF THE WEEK
        day_of_week = datetime.datetime.today().weekday()
        if day_of_week == 0:
            day_of_week = "Lunes"
        elif day_of_week == 1:
            day_of_week = "Martes"
        elif day_of_week == 2:
            day_of_week = "Miércoles"
        elif day_of_week == 3:
            day_of_week = "Jueves"
        elif day_of_week == 4:
            day_of_week = "Viernes"
        elif day_of_week == 5:
            day_of_week = "Sábado"
        elif day_of_week == 6:
            day_of_week = "Domingo"
        logs_data["dia_semana"] = day_of_week

        print(now_date, now_hour)

        # CHECK IF LAST LOG IS FROM THE SAME DAY
        last_log = Logs.objects.filter(id_estudiante=pk).order_by('-id_log')[:1]
        if last_log:
            last_log_serializer = LogsSerializer(last_log, many=True)
            if last_log_serializer.data[0]["fecha"] == now_date:
                # CHECK IF LAST LOG IS FROM THE LAST 1 MINUTE
                log_total_minutes = int(last_log_serializer.data[0]["hora"].split(":")[0]) * 60 + int(last_log_serializer.data[0]["hora"].split(":")[1])
                today_total_minutes = int(now_hour[0:2]) * 60 + int(now_hour[3:5])
                if log_total_minutes > today_total_minutes - 1:
                    return JsonResponse({'message': '¡Demasiado rápido!, espera al menos 1 minuto'}, status=status.HTTP_400_BAD_REQUEST)
                # CHECK IF LAST LOG IS IN OR OUT
                if last_log_serializer.data[0]["tipo"] == "OUT":
                    logs_data["tipo"] = "IN"
                else:
                    logs_data["tipo"] = "OUT"
            else:
                logs_data["tipo"] = "IN"

        logs_serializer = LogsSerializer(data=logs_data)
        if logs_serializer.is_valid():
            logs_serializer.save()
            return JsonResponse(logs_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(logs_serializer.errors, status=status.HTTP_400_BAD_REQUEST)