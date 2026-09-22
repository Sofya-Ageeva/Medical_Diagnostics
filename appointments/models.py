from django.db import models
from django.conf import settings


class Appointment(models.Model):
    """Запись на прием"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает подтверждения'
        CONFIRMED = 'confirmed', 'Подтверждена'
        COMPLETED = 'completed', 'Завершена'
        CANCELED = 'canceled', 'Отменена'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Пациент'
    )
    doctor = models.ForeignKey(
        'doctors.Doctor',
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='Врач'
    )
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments',
        verbose_name='Услуга'
    )
    date = models.DateField(verbose_name='Дата приема')
    time = models.TimeField(verbose_name='Время приема')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус'
    )
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name='Напоминание отправлено'
    )


    class Meta:
        verbose_name = 'Запись на прием'
        verbose_name_plural = 'Записи на прием'
        ordering = ['-date', '-time']
        unique_together = ['doctor', 'date', 'time']

    def __str__(self):
        return f"{self.user} → {self.doctor} на {self.date} {self.time}"


class ContactRequest(models.Model):
    """Заявка с формы обратной связи"""
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    message = models.TextField(verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False, verbose_name='Обработана')

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"
