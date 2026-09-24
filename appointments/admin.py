from django.contrib import admin
from .models import Appointment, ContactRequest, DiagnosticResult


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor', 'date', 'time', 'status', 'created_at']
    list_filter = ['status', 'date', 'doctor']
    search_fields = ['user__username', 'doctor__last_name']
    date_hierarchy = 'date'
    list_editable = ['status']


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at', 'is_processed']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['name', 'email']
    list_editable = ['is_processed']
    readonly_fields = ['name', 'email', 'phone', 'message', 'created_at']


@admin.register(DiagnosticResult)
class DiagnosticResultAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'created_at']
    list_filter = ['created_at']
    search_fields = ['appointment__user__email', 'conclusion']
    date_hierarchy = 'created_at'
