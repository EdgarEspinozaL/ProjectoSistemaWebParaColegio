from django.forms import ModelForm, TextInput, Textarea, NumberInput
from .models import RegistrosDiarios

class TaskForm(ModelForm):
    class Meta:
        model = RegistrosDiarios
        fields = ['title', 'description', 'stress_level']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del registro',
                'autofocus': True
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '¿Cómo te sientes hoy? Describe brevemente...'
            }),
            'stress_level': NumberInput(attrs={
                'type': 'range',
                'class': 'form-range',
                'min': 0,
                'max': 10,
                'step': 1,  
                'id':'stress_level',
            }),
        }