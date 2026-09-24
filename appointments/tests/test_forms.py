from django.test import TestCase
from django.contrib.auth import get_user_model
from appointments.forms import AppointmentForm
from doctors.models import Doctor, Specialization, TimeSlot
from datetime import date, time, timedelta

User = get_user_model()


class AppointmentFormTest(TestCase):
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
        self.future_date = date.today() + timedelta(days=7)
        self.slot = TimeSlot.objects.create(
            doctor=self.doctor,
            date=self.future_date,
            time=time(10, 0),
            is_available=True,
        )

    def test_form_valid(self):
        """Форма валидна с корректными данными"""
        form = AppointmentForm(data={
            'doctor': self.doctor.id,
            'date': self.future_date,
            'time_slot': self.slot.id,
            'comment': 'Тест',
        })
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_past_date_invalid(self):
        """Прошедшая дата недопустима"""
        past_date = date.today() - timedelta(days=1)
        form = AppointmentForm(data={
            'doctor': self.doctor.id,
            'date': past_date,
            'time_slot': self.slot.id,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Нельзя записаться на прошедшую дату.', form.errors.get('__all__', []))

    def test_form_no_slot_invalid(self):
        """Без выбранного слота — ошибка"""
        form = AppointmentForm(data={
            'doctor': self.doctor.id,
            'date': self.future_date,
            # time_slot не указан
        })
        self.assertFalse(form.is_valid())
