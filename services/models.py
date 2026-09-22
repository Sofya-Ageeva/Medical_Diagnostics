from django.db import models


class ServiceCategory(models.Model):
    """Категория услуг"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Категория услуг'
        verbose_name_plural = 'Категории услуг'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Service(models.Model):
    """Медицинская услуга"""
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='services',
        verbose_name='Категория'
    )
    name = models.CharField(max_length=200, verbose_name='Название услуги')
    slug = models.SlugField(unique=True, verbose_name='URL-идентификатор')
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание')
    full_description = models.TextField(verbose_name='Полное описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    duration = models.IntegerField(help_text='В минутах', verbose_name='Длительность')
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name
