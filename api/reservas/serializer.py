from rest_framework import serializers
from .models import Reserva
from rest_framework import serializers
from django.contrib.auth.models import User

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
class DisponibilidadeSerializer(serializers.Serializer):
    data_reserva = serializers.DateField()
    hora_reserva = serializers.TimeField()
    evento_id = serializers.UUIDField()

    

class UserRegistrationSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    class Meta:
        model = User
        fields = ['first_name', 'email', 'senha']
    
    def validate_first_name(self, value):
        # Verifica se já existe um usuário com o mesmo nome
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Já existe um usuário com este nome. Escolha um nome único.")
        return value

    def create(self, validated_data):
        # Criação do usuário usando o nome como username
        user = User.objects.create_user(
            username=validated_data['first_name'],  # O nome será usado como nome de usuário
            email=validated_data['email'],
            password=validated_data['senha']
        )
        user.save()
        return user
    