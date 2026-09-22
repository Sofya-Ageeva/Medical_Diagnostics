from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from appointments.models import Appointment
from appointments.emails import send_appointment_reminder_email


class Command(BaseCommand):
    help = 'Отправка напоминаний о приёмах на завтра'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать, кому будут отправлены напоминания, без отправки',
        )

    def handle(self, *args, **options):
        tomorrow = timezone.now().date() + timedelta(days=1)
        dry_run = options['dry_run']

        appointments = Appointment.objects.filter(
            date=tomorrow,
            status__in=['pending', 'confirmed'],
            reminder_sent=False,
        ).select_related('user', 'doctor', 'service')

        total = appointments.count()
        self.stdout.write(f' Найдено записей на {tomorrow}: {total}')

        if total == 0:
            self.stdout.write(self.style.WARNING('Нет записей для напоминания'))
            return

        sent_count = 0
        for appointment in appointments:
            if dry_run:
                self.stdout.write(
                    f'  [DRY-RUN] {appointment.user.email} — '
                    f'{appointment.time} у {appointment.doctor.full_name}'
                )
                continue

            send_appointment_reminder_email(appointment)

            appointment.reminder_sent = True
            appointment.save(update_fields=['reminder_sent'])

            sent_count += 1
            self.stdout.write(
                f'  ✅ {appointment.user.email} — '
                f'{appointment.time} у {appointment.doctor.full_name}'
            )

        if not dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'\n Отправлено напоминаний: {sent_count}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'\n[DRY-RUN] Будет отправлено: {total}')
            )
