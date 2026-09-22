from django.contrib import admin
from .models import Doctor, Specialization


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'specialization', 'experience', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['last_name', 'first_name']
    list_editable = ['is_active']
