from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    """Тесты для модели User"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123456',
            first_name='Иван',
            last_name='Петров',
            phone='+7-999-123-45-67',
        )

    def test_user_creation(self):
        """Тест создания пользователя"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Иван')
        self.assertEqual(self.user.last_name, 'Петров')
        self.assertEqual(self.user.phone, '+7-999-123-45-67')
        self.assertTrue(self.user.check_password('test123456'))

    def test_user_str(self):
        """Тест строкового представления"""
        self.assertEqual(
            str(self.user),
            'Иван Петров (testuser)'
        )

    def test_superuser_creation(self):
        """Тест создания суперпользователя"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123456',
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)

    def test_user_email_unique(self):
        """Тест уникальности email"""
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='another',
                email='test@example.com',  # Дубликат
                password='test123456',
            )
