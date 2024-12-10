from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from . import models, serializer as serializers
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.validators import ValidationError

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'nome': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do usuário'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email do usuário'),
            'senha': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário'),
        },
        required=['nome', 'email', 'senha'],
    ),
    responses={
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mensagem': openapi.Schema(type=openapi.TYPE_STRING, description='Mensagem de sucesso'),
                'usuario': openapi.Schema(type=openapi.TYPE_OBJECT, description='Dados do usuário cadastrado'),
            },
        ),
        400: 'Erro de validação',
    },
)
@api_view(['POST'])
def register_user(request):
    nome = request.data.get('nome')
    email = request.data.get('email')
    senha = request.data.get('senha')

    # Verifica se os campos obrigatórios estão presentes
    if not nome or not email or not senha:
        return Response(
            {"error": "Os campos nome, email e senha são obrigatórios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Verifica se o email já está cadastrado
    if User.objects.filter(email=email).exists():
        return Response(
            {"error": "Já existe um usuário com esse email."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Cria o usuário
    try:
        user = User.objects.create_user(username=email, email=email, password=senha)
        user.first_name = nome
        user.save()
        return Response(
            {
                "mensagem": "Usuário cadastrado com sucesso.",
                "usuario": {"id": user.id, "nome": user.first_name, "email": user.email},
            },
            status=status.HTTP_201_CREATED,
        )
    except ValidationError as e:
        return Response(
            {"error": f"Erro ao cadastrar usuário: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
@swagger_auto_schema(
    method='get',
)
@api_view(['GET'])
def getreserva(request):
    
    if request.method == 'GET':
        reserva = models.Reserva.objects.all()
        serializer = serializers.ReservaSerializer(reserva, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)

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


# novo função para verificar disponibilidade de datas e horários

from datetime import datetime

@swagger_auto_schema(
        method='post',
        request_body=serializers.DisponibilidadeSerializer
        )
@api_view(['POST'])
def verificar_disponibilidade(request):
    
    data_reserva = request.data.get('data_reserva')
    hora_reserva = request.data.get('hora_reserva')
    evento_id = request.data.get('evento_id')
    
    data = datetime.strptime(data_reserva,"%Y-%m-%d").date()
    hora = datetime.strptime(hora_reserva, "%H:%M:%S").time()
    data_hora = datetime.combine(data, hora)

    if not data_reserva or not hora_reserva or not evento_id:
        return Response({"error": "Campos obrigatórios: data_reserva, hora_reserva, evento_id"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        reserva = models.Reserva.objects.get(id= evento_id)
        print(str(data_hora)+"+00:00")
        print(reserva.data_hora_reserva.replace(microsecond=0))
        conflito = str(data_hora)+"+00:00" == str(reserva.data_hora_reserva.replace(microsecond=0))
    except reserva.DoesNotExist:
        return Response({"mensagem":"Reserva não encontrada"},status=status.HTTP_404_NOT_FOUND)
    # Verifica se há reservas conflitantes
    if conflito:
        return Response({"disponibilidade": False, "mensagem": "Data e horário já estão reservados."}, status=status.HTTP_200_OK)
    
    # Se não há conflito, a reserva pode ser feita
    return Response({"disponibilidade": True, "mensagem": "Data e horário disponíveis para reserva."}, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='put',
    request_body=serializers.DisponibilidadeSerializer
    )
@api_view(['PUT'])


def atualizar_status(self, novo_status):
        
       # Atualiza o status da reserva. #
    if novo_status in ["confirmada", "pendente", "cancelada"]:
        self.status = novo_status
    else:
        raise ValueError("Status inválido. Use: confirmada, pendente ou cancelada.")

def __str__(self):
        
    # retorna uma representação da reserva.
        
    return (f"Reserva UUID: {self.uuid}\n"
                f"Usuário: {self.usuario}\n"
                f"Data e Hora da Reserva: {self.data_hora_reserva}\n"
                f"Data e Hora do Evento: {self.data_hora_evento}\n"
                f"Descrição do Evento: {self.descricao_evento}\n"
                f"Status: {self.status}")