from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, Specialization, DoctorSchedule, TimeSlot
from django.utils import timezone



@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'specialization', 'experience', 'is_active']
    list_filter = ['specialization', 'is_active']
    search_fields = ['last_name', 'first_name']
    list_editable = ['is_active']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = [
        'doctor', 'date', 'time',
        'is_available',
        'is_available_badge', 'is_booked_badge', 'created_at'
    ]
    list_filter = ['date', 'is_available', 'doctor']
    search_fields = ['doctor__last_name', 'doctor__first_name']
    date_hierarchy = 'date'
    list_editable = ['is_available']

    fieldsets = (
        (None, {
            'fields': ('doctor', 'date', 'time', 'is_available')
        }),
    )

    def is_available_badge(self, obj):
        if obj.is_available:
            return format_html('<span style="color: green;">✅ Доступно</span>')
        return format_html('<span style="color: red;">❌ Закрыто</span>')

    is_available_badge.short_description = 'Доступность'

    def is_booked_badge(self, obj):
        if obj.is_booked():
            return format_html('<span style="color: orange;">📌 Занято</span>')
        return format_html('<span style="color: gray;">— Свободно</span>')

    is_booked_badge.short_description = 'Запись'

    actions = ['make_available', 'make_unavailable', 'generate_slots']

    @admin.action(description='✅ Открыть для записи')
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'Открыто {updated} слотов')

    @admin.action(description='❌ Закрыть для записи')
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'Закрыто {updated} слотов')

    @admin.action(description='⚡ Сгенерировать слоты на неделю')
    def generate_slots(self, request, queryset):
        """Генерация слотов для выбранных врачей"""
        from datetime import datetime, timedelta

        # Получаем уникальных врачей из выборки
        doctors = set(queryset.values_list('doctor', flat=True))

        created_count = 0
        today = timezone.now().date()

        for doctor_id in doctors:
            doctor = Doctor.objects.get(pk=doctor_id)

            # Получаем график врача
            schedules = DoctorSchedule.objects.filter(
                doctor=doctor,
                is_active=True
            )

            if not schedules.exists():
                continue

            # Генерируем слоты на 7 дней вперёд
            for day_offset in range(1, 8):
                date = today + timedelta(days=day_offset)
                weekday = date.weekday()

                # Ищем график на этот день
                try:
                    schedule = schedules.get(weekday=weekday)
                except DoctorSchedule.DoesNotExist:
                    continue

                # Генерируем временные слоты
                current = datetime.combine(date, schedule.start_time)
                end = datetime.combine(date, schedule.end_time)
                break_start = (
                    datetime.combine(date, schedule.break_start)
                    if schedule.break_start else None
                )
                break_end = (
                    datetime.combine(date, schedule.break_end)
                    if schedule.break_end else None
                )

                while current < end:
                    # Пропускаем перерыв
                    if break_start and break_end:
                        if break_start <= current < break_end:
                            current += timedelta(minutes=schedule.slot_duration)
                            continue

                    slot_time = current.time()

                    # Создаём слот, если его ещё нет
                    _, created = TimeSlot.objects.get_or_create(
                        doctor=doctor,
                        date=date,
                        time=slot_time,
                    )

                    if created:
                        created_count += 1

                    current += timedelta(minutes=schedule.slot_duration)

        self.message_user(request, f'✅ Создано {created_count} слотов')
