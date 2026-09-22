from django.db import models


class CompanyInfo(models.Model):
    """Информация о компании"""
    name = models.CharField(max_length=200, verbose_name='Название компании')
    description = models.TextField(verbose_name='Описание')
    history = models.TextField(verbose_name='История компании')
    mission = models.TextField(verbose_name='Миссия')
    values = models.TextField(verbose_name='Ценности')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    working_hours = models.CharField(max_length=100, verbose_name='Режим работы')
    logo = models.ImageField(upload_to='company/', blank=True, null=True, verbose_name='Логотип')
    map_embed = models.TextField(blank=True, verbose_name='Код карты')

    class Meta:
        verbose_name = 'Информация о компании'
        verbose_name_plural = 'Информация о компании'

    def __str__(self):
        return self.name


class Advantage(models.Model):
    """Преимущества компании"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    icon = models.CharField(max_length=50, verbose_name='Иконка (Bootstrap)')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Преимущество'
        verbose_name_plural = 'Преимущества'
        ordering = ['order']

    def __str__(self):
        return self.title
