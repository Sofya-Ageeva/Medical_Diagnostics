from django.contrib import admin
from .models import CompanyInfo, Advantage


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    """Админка для информации о компании (Singleton)"""

    list_display = ['name', 'phone', 'email']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'logo')
        }),
        ('О компании', {
            'fields': ('history', 'mission', 'values'),
            'description': 'Тексты для страницы «О компании»'
        }),
        ('Контакты', {
            'fields': ('address', 'phone', 'email', 'working_hours')
        }),
        ('Карта', {
            'fields': ('map_embed',),
            'description': 'HTML-код iframe карты проезда'
        }),
    )

    def has_add_permission(self, request):
        # Singleton — только одна запись
        return not CompanyInfo.objects.exists()


@admin.register(Advantage)
class AdvantageAdmin(admin.ModelAdmin):
    """Админка для преимуществ компании"""

    list_display = ['title', 'order', 'icon']
    list_editable = ['order']
    search_fields = ['title', 'description']
    ordering = ['order']

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'icon', 'order')
        }),
    )
