from django.urls import path
from . import views


# administrador/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.pelicula_estreno_list, name='pelicula_estreno_list'),
    path('<int:pk>/', views.pelicula_estreno_detail, name='pelicula_estreno_detail'),
    path('nueva/', views.pelicula_estreno_create, name='pelicula_estreno_create'),
    path('<int:pk>/editar/', views.pelicula_estreno_update, name='pelicula_estreno_update'),
    path('<int:pk>/eliminar/', views.pelicula_estreno_delete, name='pelicula_estreno_delete'),
]
