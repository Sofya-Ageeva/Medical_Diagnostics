from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Кастомная модель пользователя"""

    email = models.EmailField(unique=True, verbose_name='Email')

    # Персональные данные
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')  # ✅
    avatar = models.ImageField(  # ✅
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватарка'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    def get_full_name(self):
        """Полное имя пользователя"""
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username
