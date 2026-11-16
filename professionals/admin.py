from django.contrib import admin

from .models import Category, Professional, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ("full_name", "category", "neighborhood", "city", "is_active")
    list_filter = ("category", "city", "is_active")
    search_fields = ("full_name", "neighborhood", "city", "whatsapp")
    readonly_fields = ("created_at", "updated_at")
    inlines = (ServiceInline,)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "professional", "category", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "professional__full_name")
