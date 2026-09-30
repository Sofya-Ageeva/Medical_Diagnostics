from django.test import TestCase
from django.core import mail
from django.contrib.auth import get_user_model

from appointments.models import Appointment
from appointments.emails import (
    send_appointment_created_email,
    send_appointment_doctor_notification,
    send_appointment_canceled_email,
)
from doctors.models import Doctor, Specialization
from services.models import Service, ServiceCategory
from datetime import date, time


User = get_user_model()


class EmailTest(TestCase):
    """Тесты отправки email"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='patient',
            email='patient@test.ru',
            password='test123',
            first_name='Павел',
            last_name='Пациентов'
        )
        self.spec = Specialization.objects.create(name='Терапевт', slug='terapevt')
        self.doctor = Doctor.objects.create(
            first_name='Иван', last_name='Иванов',
            specialization=self.spec, experience=10,
            email='doctor@test.ru', is_active=True
        )
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            slug='diagnostika',
            order=1
        )
        self.service = Service.objects.create(
            category=self.category,
            name='Осмотр', slug='osmotr',
            price=1000, short_description='Осмотр',
            duration=30
        )
        self.appointment = Appointment.objects.create(
            user=self.user, doctor=self.doctor, service=self.service,
            date=date.today(), time=time(10, 0)
        )

    def test_send_patient_notification(self):
        mail.outbox = []
        send_appointment_created_email(self.appointment)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('patient@test.ru', mail.outbox[0].to)

    def test_send_doctor_notification(self):
        mail.outbox = []
        send_appointment_doctor_notification(self.appointment)
        self.assertEqual(len(mail.outbox), 1)

    def test_send_canceled_notification(self):
        mail.outbox = []
        send_appointment_canceled_email(self.appointment)
        self.assertEqual(len(mail.outbox), 1)
