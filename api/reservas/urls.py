from django.urls import path
from . import views
urlpatterns = [
    path('reservas/', views.getreserva ),
    path('reservas/<uuid:pk>', views.getreserva ),
    path('reservas/<int:pk>/update', views.reservaById ),
    path('reservas/<int:pk>/delete', views.reservaById ),
    path('reservas/', views.getreserva, name='getreserva'),
    path('reservas/<int:pk>/', views.reservaById, name='reservaById'),
    path('reservas/usuario/<int:usuario_id>/', views.reservas_por_usuario, name='reservas_por_usuario'),
    path('reservas/evento/<int:evento_id>/', views.reservas_por_evento, name='reservas_por_evento'),
    path('reservas/verificar/', views.verificar_disponibilidade, name='verificar_disponibilidade'),
    path('usuarios/cadastrar/', views.register_user, name='register_user'),
    path('reservas/<int:pk>/cancelar/', views.atualizar_status_reserva, name='atualizar_status_reserva'), 

]