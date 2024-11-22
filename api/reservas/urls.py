from django.urls import path
from . import views
urlpatterns = [
    path('reservas/', views.getreserva ),
    path('reservas/<uuid:pk>', views.getreserva ),
    path('reservas/<int:pk>/update', views.updatereserva ),
    path('reservas/<int:pk>/delete', views.deletereserva ),
]