from django.test import TestCase
from django.urls import reverse
from services.models import Service, ServiceCategory


class ServiceListViewTest(TestCase):
    """Тесты списка услуг"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            slug='diagnostika',
        )
        self.service1 = Service.objects.create(
            category=self.category,
            name='МРТ',
            slug='mrt',
            short_description='МРТ',
            full_description='Полное описание',
            price=5000,
            duration=30,
        )
        self.service2 = Service.objects.create(
            category=self.category,
            name='КТ',
            slug='kt',
            short_description='КТ',
            full_description='Полное описание',
            price=3000,
            duration=20,
        )
        self.url = reverse('services:list')

    def test_list_page_accessible(self):
        """Страница доступна"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/list.html')

    def test_list_shows_services(self):
        """Показывает все услуги"""
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['services']), 2)

    def test_search_filter(self):
        """Поиск по названию"""
        response = self.client.get(self.url, {'search': 'МРТ'})
        self.assertEqual(len(response.context['services']), 1)
        self.assertEqual(response.context['services'][0].name, 'МРТ')

    def test_price_filter(self):
        """Фильтр по цене"""
        response = self.client.get(self.url, {'min_price': 4000})
        self.assertEqual(len(response.context['services']), 1)
        self.assertEqual(response.context['services'][0].name, 'МРТ')

    def test_sort_by_price_asc(self):
        """Сортировка по цене (возрастание)"""
        response = self.client.get(self.url, {'sort': 'price_asc'})
        services = list(response.context['services'])
        self.assertEqual(services[0].price, 3000)
        self.assertEqual(services[1].price, 5000)

    def test_sort_by_price_desc(self):
        """Сортировка по цене (убывание)"""
        response = self.client.get(self.url, {'sort': 'price_desc'})
        services = list(response.context['services'])
        self.assertEqual(services[0].price, 5000)
        self.assertEqual(services[1].price, 3000)


class ServiceDetailViewTest(TestCase):
    """Тесты деталей услуги"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            slug='diagnostika',
        )
        self.service = Service.objects.create(
            category=self.category,
            name='МРТ',
            slug='mrt',
            short_description='МРТ',
            full_description='Полное описание',
            price=5000,
            duration=30,
        )

    def test_detail_page_accessible(self):
        url = reverse('services:detail', kwargs={'slug': 'mrt'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'services/detail.html')
        self.assertEqual(response.context['service'], self.service)

    def test_detail_404_for_unknown(self):
        url = reverse('services:detail', kwargs={'slug': 'unknown'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        