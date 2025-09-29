
from django.contrib import admin
from django.urls import path, include
from accounts.views import login_view 

urlpatterns = [
    path('', login_view, name='home'),  # Redirige la raíz al login
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]