from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Credenciales inválidas'})
    
    return render(request, 'accounts/login.html')


@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'accounts/admin_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('login')
