from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from doctors.admin import DoctorScheduleAdmin
from doctors.models import Doctor, Specialization, DoctorSchedule


class DoctorScheduleAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin = DoctorScheduleAdmin(DoctorSchedule, self.site)
        self.spec = Specialization.objects.create(name='Терапевт', slug='terapevt')
        self.doctor = Doctor.objects.create(
            first_name='Иван', last_name='Иванов',
            specialization=self.spec, experience=10, is_active=True
        )

    def test_weekday_display(self):
        """weekday_display возвращает название дня"""
        schedule = DoctorSchedule.objects.create(
            doctor=self.doctor,
            weekday=0,
            start_time='09:00',
            end_time='18:00',
            slot_duration=30,
            is_active=True
        )
        result = self.admin.weekday_display(schedule)
        self.assertEqual(result, 'Понедельник')
