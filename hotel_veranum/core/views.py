from django.shortcuts import redirect, render, get_object_or_404
from .models import Hotel, Room, Guest, Reservation, AdditionalService, Service, RestaurantOrder, InventoryItem, Provider
from .forms import GuestForm, AdditionalServiceForm, RestaurantOrderForm, ReportForm, InventoryItemForm, ProviderForm
from django.http import JsonResponse
from django.http import HttpResponse
from .transbank_config import get_transaction
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.webpay.webpay_plus.transaction import WebpayOptions
from transbank.common.integration_type import IntegrationType
import uuid
import csv



#Vistas para ingresar a un usuario #########################################################################


def home(request):
    hotels = Hotel.objects.all()  # Obtiene todos los hoteles de la base de datos
    return render(request, 'core/home.html', {'hotels': hotels})

def guest_reserva(request, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    guests = Guest.objects.filter(hotel=hotel).order_by('guest_id')
    data = {"hotel": hotel, "guests": guests}
    return render(request, "core/guest_reserva.html", data)

def guest_datos(request, hotel_id, guest_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    guest = get_object_or_404(Guest, guest_id=guest_id, hotel=hotel)
    data = {"guest": guest}
    return render(request, "core/guest_datos.html", data)

def create_guest(request):
    if request.method == "POST":
        form = GuestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('guest_reserva', hotel_id=form.cleaned_data['hotel'].hotel_id)
    else:
        form = GuestForm()

    return render(request, 'core/create_guest.html', {'form': form})

def all_guests(request):
    guests = Guest.objects.all()
    return render(request, 'core/all_guests.html', {'guests': guests})

def guest(request, action, guest_id, hotel_id):
    hotel = get_object_or_404(Hotel, hotel_id=hotel_id)
    data = {
        "mesg": "",
        "action": action,
        "guest_id": guest_id,
        "hotel_id": hotel_id
    }

    if request.method == "POST":
        if action == 'ins':
            form = GuestForm(request.POST, request.FILES)
            if form.is_valid():
                guest_instance = form.save(commit=False)
                guest_instance.hotel = hotel
                guest_instance.save()
                data["mesg"] = "¡El huésped fue creado correctamente!"
                return redirect('guest_reserva', hotel_id=hotel_id)
        elif action == 'upd':
            guest_instance = get_object_or_404(Guest, guest_id=guest_id, hotel=hotel)
            form = GuestForm(data=request.POST, files=request.FILES, instance=guest_instance)
            if form.is_valid():
                form.save()
                data["mesg"] = "¡El huésped fue actualizado correctamente!"
                return redirect('guest_reserva', hotel_id=hotel_id)
        elif action == 'del':
            guest_instance = get_object_or_404(Guest, guest_id=guest_id, hotel=hotel)
            guest_instance.delete()
            return JsonResponse({'success': True, 'mesg': '¡El huésped fue eliminado correctamente!'})

    if action == 'ins':
        data["form"] = GuestForm()
    elif action in ['upd', 'del']:
        guest_instance = get_object_or_404(Guest, guest_id=guest_id, hotel=hotel)
        if action == 'upd':
            data["form"] = GuestForm(instance=guest_instance)
        elif action == 'del':
            data["form"] = GuestForm(instance=guest_instance)

    data["list"] = Guest.objects.filter(hotel=hotel).order_by('guest_id')

    if request.is_ajax() and request.method == "POST":
        return JsonResponse({'success': True, 'mesg': data["mesg"]})

    return render(request, "core/guest.html", data)

#Vistas para servicios adicionales y restaurant ############################################################


def additional_services(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = AdditionalServiceForm(request.POST)
        if form.is_valid():
            additional_service = form.save(commit=False)
            additional_service.reservation = reservation
            additional_service.save()
            return redirect('additional_services', reservation_id=reservation_id)
    else:
        form = AdditionalServiceForm()
    
    services = AdditionalService.objects.filter(reservation=reservation)
    return render(request, 'core/additional_services.html', {'form': form, 'services': services, 'reservation': reservation})

########################### restaurant

def restaurant_order(request, reservation_id):
    # Obtener la reserva relacionada
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        form = RestaurantOrderForm(request.POST)
        if form.is_valid():
            # Crear una nueva orden de restaurante
            restaurant_order = form.save(commit=False)
            restaurant_order.reservation = reservation
            restaurant_order.save()
            return redirect('restaurant_order', reservation_id=reservation_id)
    else:
        form = RestaurantOrderForm()

    orders = RestaurantOrder.objects.filter(reservation=reservation)
    return render(request, 'core/restaurant_order.html', {
        'reservation': reservation,
        'orders': orders,
        'form': form
    })

def restaurant_order_list(request):
    orders = RestaurantOrder.objects.all()
    return render(request, 'core/restaurant_order_list.html', {'orders': orders})

def restaurant_order_create(request):
    if request.method == 'POST':
        form = RestaurantOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant_order_list')
    else:
        form = RestaurantOrderForm()
    return render(request, 'core/restaurant_order_form.html', {'form': form})

def restaurant_order_update(request, pk):
    order = get_object_or_404(RestaurantOrder, pk=pk)
    if request.method == 'POST':
        form = RestaurantOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('restaurant_order_list')
    else:
        form = RestaurantOrderForm(instance=order)
    return render(request, 'core/restaurant_order_form.html', {'form': form})

def restaurant_order_delete(request, pk):
    order = get_object_or_404(RestaurantOrder, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('restaurant_order_list')
    return render(request, 'core/restaurant_order_confirm_delete.html', {'object': order})

###### inventario del restaurant

def inventory_item_list(request):
    items = InventoryItem.objects.all()
    return render(request, 'core/inventory_item_list.html', {'items': items})

def inventory_item_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_item_list')
    else:
        form = InventoryItemForm()
    return render(request, 'core/inventory_item_form.html', {'form': form})

def inventory_item_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory_item_list')
    else:
        form = InventoryItemForm()
    return render(request, 'core/inventory_item_form.html', {'form': form})

def inventory_item_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('inventory_item_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'core/inventory_item_form.html', {'form': form})


def inventory_item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_item_list')
    return render(request, 'core/inventory_item_confirm_delete.html', {'object': item})

######################### proveedores

def provider_list(request):
    providers = Provider.objects.all()
    return render(request, 'core/provider_list.html', {'providers': providers})

def provider_create(request):
    if request.method == 'POST':
        form = ProviderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('provider_list')
    else:
        form = ProviderForm()
    return render(request, 'core/provider_form.html', {'form': form})

def provider_update(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    if request.method == 'POST':
        form = ProviderForm(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            return redirect('provider_list')
    else:
        form = ProviderForm(instance=provider)
    return render(request, 'core/provider_form.html', {'form': form})

def provider_delete(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    if request.method == 'POST':
        provider.delete()
        return redirect('provider_list')
    return render(request, 'core/provider_confirm_delete.html', {'object': provider})


# configuracion de transbank ################################################################################


def iniciar_pago(request):
    tx = get_transaction()
    response = tx.create(
        buy_order="orden12345678",
        session_id="sesion1234564",
        amount=10000,
        return_url=request.build_absolute_uri('/pago/confirmacion/')
    )
    return redirect(response['url'] + '?token_ws=' + response['token'])

def confirmacion_pago(request):
    tx = get_transaction()
    token = request.POST.get('token_ws')
    response = tx.commit(token)
    if response['status'] == 'AUTHORIZED':
        return HttpResponse("Pago exitoso")
    else:
        return HttpResponse("Pago fallido")

def pago(request):
    transaction = get_transaction()
    buy_order = str(uuid.uuid4())
    session_id = request.session.session_key
    amount = 10000  # Monto de la transacción
    return_url = request.build_absolute_uri('/pago/exito/')
    
    try:
        response = transaction.create(buy_order, session_id, amount, return_url)
        print("Response:", response)  # Añade esta línea para ver la respuesta en la consola
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except Exception as e:
        print("Error:", e)  # Añade esta línea para ver el error en la consola
        return render(request, 'error.html', {'message': str(e)})
def pago_exito(request):
    return render(request, 'pago_exito.html')


# Generación de reportes ###################################################################################

def report_selection(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report_type']
            return redirect('generate_report', report_type=report_type)
    else:
        form = ReportForm()

    return render(request, 'core/report_selection.html', {'form': form})

def generate_report(request, report_type):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'

    writer = csv.writer(response)

    if report_type == 'occupancy':
        writer.writerow(['Hotel', 'Ocupación'])
        hotels = Hotel.objects.all()
        for hotel in hotels:
            occupancy_count = Guest.objects.filter(hotel=hotel).count()
            writer.writerow([hotel.name, occupancy_count])
    elif report_type == 'guests':
        writer.writerow(['Hotel', 'ID del Huésped', 'Nombre', 'Apellido', 'Correo', 'Teléfono'])
        guests = Guest.objects.all()
        for guest in guests:
            writer.writerow([guest.hotel.name, guest.guest_id, guest.first_name, guest.last_name, guest.email, guest.phone_number])
    # Agrega más tipos de reportes según sea necesario

    return response

############################################################################################################################################################

def poblar_bd(request):
    Guest.objects.all().delete()
    Guest.objects.create(guest_id="G1", first_name='Jane',      last_name="Doe",            email="janedoe@converge.com",       phone_number="+56910001000")
    Guest.objects.create(guest_id="G2", first_name='Henry',     last_name="Ford",           email="henry@ford.com",             phone_number="+56910001001")
    Guest.objects.create(guest_id="G3", first_name='Thomas',    last_name="Wayne",          email="thomas@wayne.com",           phone_number="+56910001002")
    Guest.objects.create(guest_id="G4", first_name='Mercedes',  last_name="Sosa",           email="lanegrasosa@mecha.com",      phone_number="+56910001003")
    Guest.objects.create(guest_id="G5", first_name='Hayden',    last_name="Christensen",    email="vader@empire.com",           phone_number="+56910001004")
    Guest.objects.create(guest_id="G6", first_name='James',     last_name="Gordon",         email="jamesgordon@gcpd.com",       phone_number="+56910001005")
    Guest.objects.create(guest_id="G7", first_name='Bruce',     last_name="Wayne",          email="bruce@wayne.com",            phone_number="+56910001006")
    Guest.objects.create(guest_id="G8", first_name='Eduardo',   last_name="Alquinta",       email="gatoalquinta@jaivas.com",    phone_number="+56910001007")
    Guest.objects.create(guest_id="G9", first_name='Claudio',   last_name="Parra",          email="claudioparra@jaivas.com",    phone_number="+56910001008")
    Guest.objects.create(guest_id="G10", first_name='Tomas',   last_name="Haake",           email="tomashaake@meshuggah.com",   phone_number="+56910001009")
    return redirect(guest, action='ins', id = '-1')