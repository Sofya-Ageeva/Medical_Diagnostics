from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from doctors.models import Doctor, Specialization, TimeSlot
from appointments.models import Appointment
from datetime import date, time, timedelta
import json

User = get_user_model()


class AvailableSlotsViewTest(TestCase):
    """Тесты AJAX-эндпоинта доступных слотов"""

    def setUp(self):
        self.client = Client()
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
        self.url = reverse('appointments:available_slots')

    def test_returns_slots(self):
        """Возвращает доступные слоты"""
        response = self.client.get(self.url, {
            'doctor': self.doctor.id,
            'date': self.future_date.strftime('%Y-%m-%d'),
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertEqual(data['count'], 1)
        self.assertEqual(data['slots'][0]['time'], '10:00')

    def test_returns_empty_for_past_date(self):
        """Прошедшая дата → пустой список"""
        past_date = date.today() - timedelta(days=1)
        response = self.client.get(self.url, {
            'doctor': self.doctor.id,
            'date': past_date.strftime('%Y-%m-%d'),
        })
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)
        self.assertIn('error', data)

    def test_returns_empty_without_params(self):
        """Без параметров → 400"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_excludes_booked_slots(self):
        """Занятые слоты исключаются"""
        # Создаём запись на слот
        Appointment.objects.create(
            user=self.user,
            doctor=self.doctor,
            date=self.future_date,
            time=time(10, 0),
            status='pending',
        )

        response = self.client.get(self.url, {
            'doctor': self.doctor.id,
            'date': self.future_date.strftime('%Y-%m-%d'),
        })
        data = json.loads(response.content)
        self.assertEqual(data['count'], 0)


class AppointmentCreateViewTest(TestCase):
    """Тесты создания записи"""

    def setUp(self):
        self.client = Client()
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
        self.url = reverse('appointments:create')

    def test_requires_login(self):
        """Требует авторизации"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_create_appointment(self):
        """Успешное создание записи"""
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'doctor': self.doctor.id,
            'date': self.future_date,
            'time_slot': self.slot.id,
            'comment': 'Тест',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Appointment.objects.filter(
                user=self.user,
                doctor=self.doctor,
            ).exists()
        )
