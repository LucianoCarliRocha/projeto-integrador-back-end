from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, serializer as serializers
from drf_yasg.utils import swagger_auto_schema
@swagger_auto_schema(
    method='get',
)
@swagger_auto_schema(
    method='post',
    request_body=serializers.ReservaSerializer
)
@api_view(['GET', 'POST'])
def getreserva(request):
    if request.method == 'GET':
        reserva = models.Reserva.objects.all()
        serializer = serializers.ReservaSerializer(reserva, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = serializers.ReservaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
)
@swagger_auto_schema(
    method='put',
)
@swagger_auto_schema(
    method='delete',
)
@api_view(['GET', 'PUT', 'DELETE'])
def reservaById(request, pk):
    try:
        reserva = models.reserva.objects.get(id=pk)
    except models.reserva.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = serializers.ReservaSerializer(reserva)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = serializers.ReservaSerializer(reserva, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        reserva.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@swagger_auto_schema(method='get')
@api_view(['GET'])
def reservas_por_usuario(request, usuario_id):
    reservas = models.reserva.objects.filter(usuario_id=usuario_id).order_by('data_reserva')
    serializer = serializers.ReservaSerializer(reservas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Visualizar reservas de um evento ou espaço específico
@swagger_auto_schema(method='get')
@api_view(['GET'])
def reservas_por_evento(request, evento_id):
    reservas = models.reserva.objects.filter(evento_id=evento_id).order_by('data_reserva')
    serializer = serializers.ReservaSerializer(reservas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)