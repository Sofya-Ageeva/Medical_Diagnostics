from django.test import TestCase
from django.urls import reverse
from django.contrib import admin
from django.contrib.admin.sites import AdminSite

from .models import CompanyInfo, Advantage
from .admin import CompanyInfoAdmin


class MainViewsTest(TestCase):
    """Тесты views главного приложения"""

    def setUp(self):
        self.company = CompanyInfo.objects.create(
            name='МедДиагностика',
            description='Современный медицинский центр',
            history='Основана в 2010 году',
            mission='Качественная диагностика',
            values='Профессионализм, забота',
            address='г. Москва, ул. Примерная, 10',
            phone='+7 (495) 123-45-67',
            email='info@test.ru',
            working_hours='Пн-Пт 8:00-20:00',
        )

    def test_home_view_status(self):
        """Главная открывается"""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_contains_company(self):
        """Главная показывает описание компании"""
        response = self.client.get(reverse('main:home'))
        self.assertContains(response, 'Современный медицинский центр')

    def test_about_view(self):
        """О компании показывает историю"""
        response = self.client.get(reverse('main:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Основана в 2010')

    def test_contacts_view(self):
        """Контакты показывает адрес"""
        response = self.client.get(reverse('main:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'г. Москва')

    def test_home_contains_advantages(self):
        """Главная показывает преимущества"""
        Advantage.objects.create(
            title='Опытные специалисты',
            description='Более 50 врачей',
            icon='person-badge',
            order=1
        )
        response = self.client.get(reverse('main:home'))
        self.assertContains(response, 'Опытные специалисты')


class MainAdminTest(TestCase):
    """Тесты админки главного приложения"""

    def test_admin_registered(self):
        """Модели зарегистрированы в админке"""
        self.assertIn(CompanyInfo, admin.site._registry)
        self.assertIn(Advantage, admin.site._registry)

    def test_company_info_singleton(self):
        """CompanyInfo — Singleton (нельзя добавить два)"""
        site = AdminSite()
        admin_instance = CompanyInfoAdmin(CompanyInfo, site)
        # Изначально можно добавить
        self.assertTrue(admin_instance.has_add_permission(None))
        # Создаём запись
        CompanyInfo.objects.create(name='Первая')
        # Теперь нельзя
        self.assertFalse(admin_instance.has_add_permission(None))
