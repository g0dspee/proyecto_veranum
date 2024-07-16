from django.shortcuts import redirect, render, get_object_or_404
from .models import Hotel, Room, Guest, Reservation, AdditionalService, RestaurantOrder, Service, Provider
from .forms import GuestForm, AdditionalServiceForm, RestaurantOrderForm
from django.http import JsonResponse
from django.http import HttpResponse
from .transbank_config import get_transaction
from transbank.webpay.webpay_plus.transaction import Transaction
from transbank.webpay.webpay_plus.transaction import WebpayOptions
from transbank.common.integration_type import IntegrationType




#Vistas para ingresar a un usuario


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
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest_instance = form.save()
            return redirect('guest_reserva', hotel_id=guest_instance.hotel.hotel_id)
    else:
        form = GuestForm()

    return render(request, 'core/create_guest.html', {'form': form})


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

#Vistas para servicios adicionales y restaurant


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


def restaurant_order(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = RestaurantOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.reservation = reservation
            order.save()
            return redirect('restaurant_order', reservation_id=reservation_id)
    else:
        form = RestaurantOrderForm()

    orders = RestaurantOrder.objects.filter(reservation=reservation)
    return render(request, 'core/restaurant_order.html', {'form': form, 'orders': orders, 'reservation': reservation})



# configuracion de transbank


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