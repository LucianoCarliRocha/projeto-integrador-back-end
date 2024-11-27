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
]

