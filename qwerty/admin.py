from django.contrib import admin
from .models import (
    Customer, Genre, Label, Artist, Album, AlbumArtist, Track,
    Order, OrderItem, Employee, Sale, Payment, Supplier,
    Shipment, Inventory, UserProfile
)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ()

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name',)
    list_filter = ('country',)

class AlbumArtistInline(admin.TabularInline):
    model = AlbumArtist
    extra = 1

class TrackInline(admin.TabularInline):
    model = Track
    extra = 1

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_date', 'price', 'label', 'genre')
    list_filter = ('genre', 'label', 'release_date')
    search_fields = ('title',)
    inlines = [AlbumArtistInline, TrackInline]

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order_date', 'total_amount')
    list_filter = ('order_date',)
    search_fields = ('customer__first_name', 'customer__last_name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'album', 'quantity', 'price_at_purchase')
    list_filter = ('album',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'position')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('position',)

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('order', 'employee', 'sale_date')
    list_filter = ('sale_date', 'employee')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_date', 'amount', 'payment_method')
    list_filter = ('payment_date', 'payment_method')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'phone', 'email', 'country')
    search_fields = ('name', 'contact_name')
    list_filter = ('country',)

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'album', 'quantity', 'shipment_date')
    list_filter = ('shipment_date', 'supplier')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('album', 'stock_quantity', 'last_updated')
    list_filter = ('last_updated',)
    search_fields = ('album__title',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)
