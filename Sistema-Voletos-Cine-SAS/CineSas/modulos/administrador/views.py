from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from modulos.boletos.models import PeliculaEstreno
from .forms import PeliculaEstrenoForm
from django.contrib.auth.decorators import login_required




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/peliculas/')  # Redirigir a la página de inicio o a otra vista
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'administrador/login.html')



# administrador/views.py

@login_required
def pelicula_estreno_list(request):
    peliculas = PeliculaEstreno.objects.all()
    return render(request, 'administrador/pelicula_estreno_list.html', {'peliculas': peliculas})

@login_required
def pelicula_estreno_detail(request, pk):
    pelicula = get_object_or_404(PeliculaEstreno, pk=pk)
    return render(request, 'administrador/pelicula_estreno_detail.html', {'pelicula': pelicula})

@login_required
def pelicula_estreno_create(request):
    if request.method == "POST":
        form = PeliculaEstrenoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pelicula_estreno_list')
    else:
        form = PeliculaEstrenoForm()
    return render(request, 'administrador/pelicula_estreno_form.html', {'form': form})

@login_required
def pelicula_estreno_update(request, pk):
    pelicula = get_object_or_404(PeliculaEstreno, pk=pk)
    if request.method == "POST":
        form = PeliculaEstrenoForm(request.POST, request.FILES, instance=pelicula)
        if form.is_valid():
            form.save()
            return redirect('pelicula_estreno_list')
    else:
        form = PeliculaEstrenoForm(instance=pelicula)
    return render(request, 'administrador/pelicula_estreno_form.html', {'form': form})

@login_required
def pelicula_estreno_delete(request, pk):
    pelicula = get_object_or_404(PeliculaEstreno, pk=pk)
    if request.method == "POST":
        pelicula.delete()
        return redirect('pelicula_estreno_list')
    return render(request, 'administrador/pelicula_estreno_confirm_delete.html', {'pelicula': pelicula})



