from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


def send_appointment_created_email(appointment):
    """Отправка письма пациенту о создании записи"""
    subject = f'Запись на приём создана — {appointment.date} {appointment.time}'
    html_content = render_to_string('emails/appointment_created.html', {
        'appointment': appointment,
    })
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.user.email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=True)


def send_appointment_doctor_notification(appointment):
    """Отправка письма врачу о новой записи"""
    if not appointment.doctor.email:
        return

    subject = f'Новая запись — {appointment.user.get_full_name()} на {appointment.date}'

    html_content = render_to_string('emails/appointment_doctor.html', {
        'appointment': appointment,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.doctor.email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=True)


def send_appointment_reminder_email(appointment):
    """Отправка напоминания пациенту"""
    subject = f'🔔 Напоминание: завтра приём у {appointment.doctor.full_name}'

    html_content = render_to_string('emails/appointment_reminder.html', {
        'appointment': appointment,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.user.email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=True)


def send_appointment_canceled_email(appointment):
    """Отправка письма об отмене записи"""
    subject = f'Запись отменена — {appointment.date} {appointment.time}'

    html_content = render_to_string('emails/appointment_canceled.html', {
        'appointment': appointment,
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [appointment.user.email],
    )
    email.attach_alternative(html_content, 'text/html')
    email.send(fail_silently=True)
