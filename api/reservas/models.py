from django.db import models
from django.contrib.auth.models import User

import uuid
from datetime import datetime

class Reserva(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    data_hora_reserva = models.DateTimeField() 
    data_hora_evento = models.DateTimeField()  
    descricao_evento = models.TextField()
