from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('habitaciones/', views.habitaciones, name='habitaciones'),

    path('habitaciones/matrimonial/', views.habitacion_matrimonial, name='habitacion_matrimonial'),
    path('habitaciones/triple/', views.habitacion_triple, name='habitacion_triple'),
    path('habitaciones/cuadruple/', views.habitacion_cuadruple, name='habitacion_cuadruple'),
    path('habitaciones/quintuple/', views.habitacion_quintuple, name='habitacion_quintuple'),
    path('habitaciones/sextuple/', views.habitacion_sextuple, name='habitacion_sextuple'),
    path('habitaciones/septuple/', views.habitacion_septuple, name='habitacion_septuple'),



    path('servicios/', views.servicios, name='servicios'),
    path('reservas/', views.reservas, name='reservas'),

    #galeria y diviciones
    path('galeria/', views.galeria, name='galeria'),


    
    path('paquetes/', views.paquetes, name='paquetes'),

    path('api/google-reviews/', views.get_google_reviews, name='google_reviews'),
]
