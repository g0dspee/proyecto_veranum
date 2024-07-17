from django.db import models

    
class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, primary_key=True)
    room_type = models.CharField(max_length=50)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.hotel.name} - {self.room_number}"

class Guest(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    guest_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def __str__(self):
        return f"Reserva para {self.guest} en {self.room}"
    
    def total_days(self):
        return (self.check_out - self.check_in).days

    def calculate_total_price(self):
        total_price = self.room.price * self.total_days()
        additional_services_cost = sum(service.service.price * service.quantity for service in self.additionalservice_set.all())
        total_price += additional_services_cost * self.total_days()
        return total_price
    
###########################################################################################################

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class AdditionalService(models.Model):
    RESERVATION_STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=RESERVATION_STATUS_CHOICES, default='requested')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.service.name} para Reserva {self.reservation.id}"
    
############################################################################################################

class Provider(models.Model):
    name = models.CharField(max_length=100)
    contact_info = models.TextField()

    def __str__(self):
        return self.name

class RestaurantOrder(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Order for Reservation {self.reservation.id} from {self.provider.name}"
    
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    

#### Actividades ########################################################################################################

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('social', 'Social'),
        ('corporate', 'Corporativo'),
        ('gastronomic', 'Gastronomico'),
        ('cultural', 'Cultural'),
        ('thematic', 'Temático'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    details = models.TextField()

    def __str__(self):
        return f"{self.activity_type} En {self.hotel.name} el {self.date} a las {self.time}"