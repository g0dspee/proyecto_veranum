from django import forms
from django.forms import ModelForm, fields
from .models import Guest, Hotel, AdditionalService, RestaurantOrder, InventoryItem, Provider, Activity

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
        widgets = {
            'hotel': forms.Select(attrs={'class': 'form-control'})
        }

    hotel = forms.ModelChoiceField(queryset=Hotel.objects.all(), label="Hotel", required=True)

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

class ReportForm(forms.Form):
    REPORT_CHOICES = [
        ('occupancy', 'Reporte de Ocupación'),
        ('guests', 'Reporte de Huéspedes'),
        # Agrega más tipos de reportes según sea necesario
    ]
    report_type = forms.ChoiceField(choices=REPORT_CHOICES, label="Tipo de Reporte")

class RestaurantOrderForm(forms.ModelForm):
    class Meta:
        model = RestaurantOrder
        fields = ['reservation', 'provider', 'delivery_date', 'total_amount', 'status']
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'quantity', 'unit_price', 'provider']

class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = ['name', 'contact_info']
        labels = {
            'name': 'Nombre del Proveedor',
            'contact_info': 'Información de Contacto',
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['hotel', 'date', 'time', 'activity_type', 'details']
        labels = {
            'hotel': 'Hotel',
            'date': 'Fecha',
            'time': 'Hora',
            'activity_type': 'Tipo de Actividad',
            'details': 'Detalle de la Actividad',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'activity_type': forms.Select(choices=Activity.ACTIVITY_TYPES),
            'details': forms.Textarea(attrs={'rows': 4}),
        }