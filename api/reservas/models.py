from django.db import models
from django.contrib.auth.models import User

import uuid
from datetime import datetime

class Reserva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKeyfield(User, on_delete=models.CASCADE)  # Referência ao usuário (pode ser um objeto ou ID)
    data_hora_reserva = models.DateTimeField()  # Data e hora da reserva (agora)
    data_hora_evento = models.DateTimeField()  # Data e hora do evento
    descricao_evento = models.TextField()  # Descrição do evento

    # def atualizar_status(self, novo_status):
    #     """
    #     Atualiza o status da reserva.
    #     """
    #     if novo_status in ["confirmada", "pendente", "cancelada"]:
    #         self.status = novo_status
    #     else:
    #         raise ValueError("Status inválido. Use: confirmada, pendente ou cancelada.")

    # def __str__(self):
    #     """
    #     Retorna uma representação legível da reserva.
    #     """
    #     return (f"Reserva UUID: {self.uuid}\n"
    #             f"Usuário: {self.usuario}\n"
    #             f"Data e Hora da Reserva: {self.data_hora_reserva}\n"
    #             f"Data e Hora do Evento: {self.data_hora_evento}\n"
    #             f"Descrição do Evento: {self.descricao_evento}\n"
    #             f"Status: {self.status}")