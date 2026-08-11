from django.contrib import admin
from .models import Category, Service, Realization, Product, Order, OrderItem, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'slug', 'icon')
    list_filter = ('type',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'icon', 'is_featured', 'is_active', 'order', 'created_at')
    list_filter = ('is_featured', 'is_active', 'category')
    search_fields = ('title', 'short_description', 'full_description')
    list_editable = ('is_featured', 'is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Realization)
class RealizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'client_name', 'completion_date', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active', 'category')
    search_fields = ('title', 'client_name', 'tech_stack', 'short_description')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'badge', 'is_featured', 'is_active')
    list_filter = ('category', 'is_featured', 'is_active', 'badge')
    search_fields = ('name', 'short_description', 'full_description')
    list_editable = ('price', 'discount_price', 'stock', 'badge', 'is_featured', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'subtotal')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_phone', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email', 'customer_phone', 'city')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at', 'total_amount')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'service_interest', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
