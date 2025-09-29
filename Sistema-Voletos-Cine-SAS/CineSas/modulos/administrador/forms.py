# administrador/forms.py
from django import forms
from modulos.boletos.models import PeliculaEstreno

class PeliculaEstrenoForm(forms.ModelForm):
    class Meta:
        model = PeliculaEstreno
        fields = ['titulo', 'descripcion', 'duracion', 'imagen', 'fecha_estreno']
