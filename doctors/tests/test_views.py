from django.test import TestCase
from django.urls import reverse
from doctors.models import Doctor, Specialization


class DoctorViewsTest(TestCase):
    """Тесты views приложения doctors"""

    def setUp(self):
        self.spec = Specialization.objects.create(
            name='Терапевт',
            slug='terapevt'
        )
        self.doctor = Doctor.objects.create(
            first_name='Иван',
            last_name='Иванов',
            specialization=self.spec,
            experience=15,
            is_active=True
        )

    def test_doctor_list(self):
        """Список врачей открывается"""
        response = self.client.get(reverse('doctors:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иванов')

    def test_doctor_detail(self):
        """Детали врача открываются"""
        response = self.client.get(reverse('doctors:detail', args=[self.doctor.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Иванов')

    def test_doctor_by_specialization(self):
        """Фильтр по специализации работает"""
        response = self.client.get(
            reverse('doctors:specialization', args=['terapevt'])
        )
        self.assertEqual(response.status_code, 200)
