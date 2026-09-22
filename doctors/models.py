from django.db import models
from django.utils.text import slugify

TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    ' ': '-',
}


def transliterate(text):
    """Транслитерация русского текста в латиницу"""
    result = []
    for char in text.lower():
        result.append(TRANSLIT.get(char, char))
    return ''.join(result)


class Specialization(models.Model):
    """Специализация врача"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True,        # ✅ Добавлено — позволяет NULL для существующих записей
        verbose_name='URL-идентификатор'
    )
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализации'

    def save(self, *args, **kwargs):
        """Автогенерация slug из name"""
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    """Врач"""
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    email = models.EmailField(blank=True, verbose_name='Email')
    specialization = models.ForeignKey(
        Specialization,
        on_delete=models.CASCADE,
        related_name='doctors',
        verbose_name='Специализация'
    )
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True, verbose_name='Фото')
    experience = models.IntegerField(verbose_name='Опыт работы (лет)')
    education = models.TextField(verbose_name='Образование')
    bio = models.TextField(verbose_name='Биография')
    is_active = models.BooleanField(default=True, verbose_name='Работает')

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} ({self.specialization})"

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()
