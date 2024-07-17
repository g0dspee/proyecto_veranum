from django.urls import path
from .views import home, guest_reserva, all_guests, guest, create_guest, reservation_list, additional_services, reservation_detail, restaurant_order, restaurant_order_list, restaurant_order_create, restaurant_order_update, restaurant_order_delete, inventory_item_list, inventory_item_create, inventory_item_update, inventory_item_delete, provider_list, provider_create, provider_update, provider_delete, iniciar_pago, confirmacion_pago, pago_exito, report_selection, generate_report, activity_list, activity_create, activity_update, activity_delete

urlpatterns = [
    path('', home, name="home"),
    path('hotel_veranum/<int:hotel_id>/guests/', guest_reserva, name='guest_reserva'),  # URL para listar huéspedes
    path('guest/<str:action>/<int:guest_id>/<int:hotel_id>/', guest, name='guest'),
    path('all_guests/', all_guests, name='all_guests'),  # Nueva URL
    path('guest/<str:action>/<int:guest_id>/<int:hotel_id>/', guest, name='guest'),  # URL para crear, actualizar o eliminar un huésped
    path('guest/create/', create_guest, name='guest_form'),  # URL para la creación de un nuevo huésped
    path('reservations/', reservation_list, name='reservation_list'),
    path('reservation/<int:reservation_id>/', reservation_detail, name='reservation_detail'),
    path('reservation/<int:reservation_id>/additional_services/', additional_services, name='additional_services'),  # URL para servicios adicionales
    path('reservation/<int:reservation_id>/restaurant_order/', restaurant_order, name='restaurant_order'),  # URL para órdenes de restaurante
    path('pago/', iniciar_pago, name='iniciar_pago'),
    path('pago/confirmacion/', confirmacion_pago, name='confirmacion_pago'),
    path('pago/exito/', pago_exito, name='pago_exito'),
    path('report_selection/', report_selection, name='report_selection'),
    path('generate_report/<str:report_type>/', generate_report, name='generate_report'),
    path('restaurant/orders/', restaurant_order_list, name='restaurant_order_list'),
    path('restaurant_order/create/', restaurant_order_create, name='create_restaurant_order'),
    path('restaurant/order/<int:pk>/update/', restaurant_order_update, name='restaurant_order_update'),
    path('restaurant/order/<int:pk>/delete/', restaurant_order_delete, name='restaurant_order_delete'),
    path('inventory/items/', inventory_item_list, name='inventory_item_list'),
    path('inventory/item/create/', inventory_item_create, name='inventory_item_create'),
    path('inventory/item/<int:pk>/update/', inventory_item_update, name='inventory_item_update'),
    path('inventory/item/<int:pk>/delete/', inventory_item_delete, name='inventory_item_delete'),
    path('providers/', provider_list, name='provider_list'),
    path('provider/create/', provider_create, name='provider_create'),
    path('provider/<int:pk>/update/', provider_update, name='provider_update'),
    path('provider/<int:pk>/delete/', provider_delete, name='provider_delete'),
    path('activities/', activity_list, name='activity_list'),
    path('activities/create/', activity_create, name='activity_create'),
    path('activities/<int:activity_id>/update/', activity_update, name='activity_update'),
    path('activities/<int:activity_id>/delete/', activity_delete, name='activity_delete'),
]

