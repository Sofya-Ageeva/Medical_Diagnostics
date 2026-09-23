from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationViewTest(TestCase):
    """Тесты регистрации"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('users:register')

    def test_register_page_accessible(self):
        """Страница регистрации доступна"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_user_success(self):
        """Успешная регистрация"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'first_name': 'Новый',
            'last_name': 'Пользователь',
            'phone': '+7-999-111-22-33',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_duplicate_email(self):
        """Регистрация с существующим email"""
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='test123456',
        )

        data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Дубликат
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())


class LoginViewTest(TestCase):
    """Тесты входа"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123456',
        )
        self.url = reverse('users:login')

    def test_login_page_accessible(self):
        """Страница входа доступна"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        """Успешный вход"""
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'test123456',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        """Вход с неправильным паролем"""
        response = self.client.post(self.url, {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    """Тесты профиля"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123456',
        )
        self.url = reverse('users:profile')

    def test_profile_requires_login(self):
        """Профиль требует авторизации"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Редирект на логин

    def test_profile_accessible_after_login(self):
        """Профиль доступен после входа"""
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        """Обновление профиля"""
        self.client.force_login(self.user)
        response = self.client.post(self.url, {
            'first_name': 'Обновленное',
            'last_name': 'Имя',
            'email': 'updated@example.com',
            'phone': '+7-999-999-99-99',
        })
        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Обновленное')
        