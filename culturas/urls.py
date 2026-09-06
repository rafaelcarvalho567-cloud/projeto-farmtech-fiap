from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('nova/', views.nova_cultura, name='nova_cultura'),
    path('editar/<int:pk>/', views.editar_cultura, name='editar_cultura'),
    path('deletar/<int:pk>/', views.deletar_cultura, name='deletar_cultura'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('clima/', views.clima, name='clima'),
    path('api/clima/', views.clima_api, name='clima_api'),
    path('api/geocode/', views.geocode, name='geocode'),
]
