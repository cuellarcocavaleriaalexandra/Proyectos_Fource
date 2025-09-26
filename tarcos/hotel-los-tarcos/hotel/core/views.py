from django.shortcuts import render
import os
from django.conf import settings
from django.http import JsonResponse
from django.conf import settings
import requests
import json

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def habitaciones(request):
    return render(request, 'core/habitaciones.html')

def servicios(request):
    return render(request, 'core/servicios.html')

def reservas(request):
    return render(request, 'core/reservas.html')

def galeria(request):
    base_static_path = os.path.join(settings.BASE_DIR, 'core', 'static', 'images')
    
    # Videos
    video_path = os.path.join(base_static_path, 'video')
    video_names = []
    allowed_video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.webm'}
    try:
        if os.path.exists(video_path):
            video_names = [
                f for f in os.listdir(video_path)
                if os.path.isfile(os.path.join(video_path, f)) and
                os.path.splitext(f.lower())[1] in allowed_video_extensions
            ]
    except OSError:
        pass

    # Imágenes de galería
    galeria_path = os.path.join(base_static_path, 'galeria')
    galeria_images = []
    allowed_image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.avif'}
    try:
        if os.path.exists(galeria_path):
            galeria_images = [
                f for f in os.listdir(galeria_path)
                if os.path.isfile(os.path.join(galeria_path, f)) and
                os.path.splitext(f.lower())[1] in allowed_image_extensions
            ]
    except OSError:
        pass

    # Imágenes de huéspedes
    huespedes_path = os.path.join(base_static_path, 'huespedes')
    huespedes_images = []
    try:
        if os.path.exists(huespedes_path):
            huespedes_images = [
                f for f in os.listdir(huespedes_path)
                if os.path.isfile(os.path.join(huespedes_path, f)) and
                os.path.splitext(f.lower())[1] in allowed_image_extensions
            ]
    except OSError:
        pass

    return render(request, 'core/galeria.html', {
        'video_names': video_names,
        'galeria_images': galeria_images,
        'huespedes_images': huespedes_images
    })





def paquetes(request):
    return render(request, 'core/paquetes.html')


#Habitaciones



def habitacion_matrimonial(request):
    return render(request, 'core/habitacion_matrimonial.html')

def habitacion_triple(request):
    return render(request, 'core/habitacion_triple.html')

def habitacion_cuadruple(request):
    return render(request, 'core/habitacion_cuadruple.html')

def habitacion_quintuple(request):
    return render(request, 'core/habitacion_quintuple.html')

def habitacion_sextuple(request):
    return render(request, 'core/habitacion_sextuple.html')

def habitacion_septuple(request):
    return render(request, 'core/habitacion_septuple.html')


#MAPS COMENTARIOS
def get_google_reviews(request):
    if not hasattr(settings, 'GOOGLE_MAPS_API_KEY'):
        return JsonResponse({
            'success': False,
            'error': 'API key not configured'
        })
    
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    
    params = {
        'place_id': "ChIJAT2CDvbP-5MRayYoDNnpB94",
        'fields': 'name,rating,user_ratings_total,reviews',
        'key': settings.GOOGLE_MAPS_API_KEY,
        'language': 'es'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get('status') == 'OK':
            return JsonResponse({
                'success': True,
                'data': data['result']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': data.get('status')
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })