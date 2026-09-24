from django.test import TestCase
from services.models import Service, ServiceCategory


class ServiceCategoryModelTest(TestCase):
    """Тесты для модели ServiceCategory"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            slug='diagnostika',
            description='Диагностические услуги',
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Диагностика')
        self.assertEqual(self.category.slug, 'diagnostika')

    def test_category_str(self):
        self.assertEqual(str(self.category), 'Диагностика')


class ServiceModelTest(TestCase):
    """Тесты для модели Service"""

    def setUp(self):
        self.category = ServiceCategory.objects.create(
            name='Диагностика',
            slug='diagnostika',
        )
        self.service = Service.objects.create(
            category=self.category,
            name='МРТ',
            slug='mrt',
            short_description='Магнитно-резонансная томография',
            full_description='Полное описание МРТ',
            price=5000,
            duration=30,
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, 'МРТ')
        self.assertEqual(self.service.price, 5000)
        self.assertEqual(self.service.duration, 30)
        self.assertTrue(self.service.is_active)

    def test_service_str(self):
        self.assertEqual(str(self.service), 'МРТ')

    def test_service_category_relation(self):
        self.assertEqual(self.service.category, self.category)
        self.assertIn(self.service, self.category.services.all())
