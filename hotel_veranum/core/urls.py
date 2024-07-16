from django.urls import path
from .views import home, guest_reserva, guest_datos, guest, create_guest, additional_services, restaurant_order, iniciar_pago, confirmacion_pago

urlpatterns = [
    path('', home, name="home"),
    path('hotel_veranum/<int:hotel_id>/guests/', guest_reserva, name='guest_reserva'),  # URL para listar huéspedes
    path('guest_datos/<int:guest_id>/', guest_datos, name='guest_datos'),
    path('guest/<str:action>/<int:guest_id>/<int:hotel_id>/', guest, name='guest'),  # URL para crear, actualizar o eliminar un huésped
    path('guest/create/', create_guest, name='guest_form'),  # URL para la creación de un nuevo huésped
    path('reservation/<int:reservation_id>/additional_services/', additional_services, name='additional_services'),  # URL para servicios adicionales
    path('reservation/<int:reservation_id>/restaurant_order/', restaurant_order, name='restaurant_order'),  # URL para órdenes de restaurante
    path('pago/', iniciar_pago, name='iniciar_pago'),
    path('pago/confirmacion/', confirmacion_pago, name='confirmacion_pago'),
]