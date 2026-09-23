from django.test import TestCase
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Specialization, TimeSlot
from appointments.models import Appointment
from datetime import date, time

User = get_user_model()


class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123456',
        )
        self.spec = Specialization.objects.create(name='Терапевт')
        self.doctor = Doctor.objects.create(
            last_name='Иванов',
            first_name='Иван',
            specialization=self.spec,
            experience=10,
            education='МГМУ',
            bio='Опытный врач',
        )
        self.appointment = Appointment.objects.create(
            user=self.user,
            doctor=self.doctor,
            date=date(2026, 12, 1),
            time=time(10, 0),
            status='pending',
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.user, self.user)
        self.assertEqual(self.appointment.doctor, self.doctor)
        self.assertEqual(self.appointment.status, 'pending')
        self.assertFalse(self.appointment.reminder_sent)

    def test_appointment_str(self):
        self.assertIn('Иванов', str(self.appointment))

    def test_appointment_status_choices(self):
        self.assertEqual(Appointment.Status.PENDING, 'pending')
        self.assertEqual(Appointment.Status.CONFIRMED, 'confirmed')
        self.assertEqual(Appointment.Status.COMPLETED, 'completed')
        self.assertEqual(Appointment.Status.CANCELED, 'canceled')
