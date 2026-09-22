from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Appointment
from .emails import (
    send_appointment_created_email,
    send_appointment_doctor_notification,
    send_appointment_canceled_email,
)


@receiver(post_save, sender=Appointment)
def appointment_created(sender, instance, created, **kwargs):
    """При создании записи — отправляет письма"""
    if created:
        # ✅ Письмо пациенту
        send_appointment_created_email(instance)

        # ✅ Письмо врачу
        send_appointment_doctor_notification(instance)


@receiver(pre_delete, sender=Appointment)
def appointment_canceled(sender, instance, **kwargs):
    """При удалении записи — отправляет письмо"""
    send_appointment_canceled_email(instance)