from datetime import datetime, timedelta
from doctors.models import DoctorSchedule
from .models import Appointment


def get_available_slots(doctor, date):
    """Возвращает список доступных слотов для врача на указанную дату."""
    weekday = date.weekday()

    # Ищем график врача на этот день
    try:
        schedule = DoctorSchedule.objects.get(
            doctor=doctor,
            weekday=weekday,
            is_active=True
        )
    except DoctorSchedule.DoesNotExist:
        return []

    slots = []
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
        slot_time = current.time()

        if break_start and break_end:
            if break_start <= current < break_end:
                current += timedelta(minutes=schedule.slot_duration)
                continue

        slots.append(slot_time)
        current += timedelta(minutes=schedule.slot_duration)

    # Исключаем занятые слоты
    busy_slots = Appointment.objects.filter(
        doctor=doctor,
        date=date,
        status__in=['pending', 'confirmed']
    ).values_list('time', flat=True)

    available = [
        slot for slot in slots
        if slot not in busy_slots
    ]

    today = datetime.now().date()
    if date == today:
        now = datetime.now().time()
        available = [slot for slot in available if slot > now]

    return available