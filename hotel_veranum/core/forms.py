from django import forms
from django.forms import ModelForm, fields
from .models import Guest, Hotel, AdditionalService, RestaurantOrder

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['guest_id', 'first_name', 'last_name', 'email', 'phone_number', 'hotel']
        labels = {
            'guest_id': 'ID del Huésped',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'phone_number': 'Número de Teléfono',
            'hotel': 'Hotel',
        }

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label="Hotel")

class AdditionalServiceForm(forms.ModelForm):
    class Meta:
        model = AdditionalService
        fields = ['service', 'quantity']
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'service': 'Servicio Adicional',
            'quantity': 'Cantidad',
        }

class RestaurantOrderForm(forms.ModelForm):
    class Meta:
        model = RestaurantOrder
        fields = ['provider', 'delivery_date', 'total_amount']
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'delivery_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'total_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'provider': 'Proveedor',
            'delivery_date': 'Fecha de Entrega',
            'total_amount': 'Monto Total',
        }