from django.contrib import admin
from .models import Room, Guest, Reservation, Hotel, Service, AdditionalService, RestaurantOrder, Provider

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'hotel', 'capacity', 'price']
    search_fields = ['room_number', 'hotel__name']

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['guest_id', 'first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name', 'email']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['guest', 'room', 'check_in', 'check_out']
    search_fields = ['guest__first_name', 'guest__last_name', 'room__room_number']

class HotelFilter(admin.SimpleListFilter):
    title = 'hotel'
    parameter_name = 'hotel'

    def lookups(self, request, model_admin):
        return [(hotel.id, hotel.name) for hotel in Hotel.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(hotel_id=self.value())
        return queryset

# Registering Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price')
    search_fields = ('name', 'description')

# Registering AdditionalService model
@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'service', 'status', 'quantity')
    list_filter = ('status', 'service')
    search_fields = ('reservation__id', 'service__name')
    raw_id_fields = ('reservation', 'service')

# Registering RestaurantOrder model
@admin.register(RestaurantOrder)
class RestaurantOrderAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'provider', 'order_date', 'delivery_date', 'total_amount', 'status')
    list_filter = ('status', 'provider')
    search_fields = ('reservation__id', 'provider__name')
    raw_id_fields = ('reservation', 'provider')
    date_hierarchy = 'order_date'

# Registering Provider model
@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info')
    search_fields = ('name', 'contact_info')