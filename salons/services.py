from datetime import datetime, timedelta
from django.utils import timezone
from .models import Appointment

def get_available_slots(salon, service, selected_date):
    # Get the salon's opening and closing times
    current_timezone = timezone.get_current_timezone()
    opening_datetime = timezone.make_aware(datetime.combine(selected_date, salon.opening_time), current_timezone)
    closing_datetime = timezone.make_aware(datetime.combine(selected_date, salon.closing_time), current_timezone)

    service_duration = timedelta(minutes=service.duration_minutes)
    buffer_duration = timedelta(minutes=salon.buffer_time_minutes)
    slot_interval = timedelta(minutes=salon.booking_interval_minutes)

    appointments = Appointment.objects.filter(
        salon=salon,
        status='confirmed',
        start_time__lt = closing_datetime,
        end_time__gt = opening_datetime
    )

    available_slots = []
    current_start = opening_datetime

    while current_start + service_duration <= closing_datetime:
        current_end = current_start + service_duration + buffer_duration

        overlaps = any(
            appointment.start_time < current_end and appointment.end_time > current_start for appointment in appointments
        )

        if not overlaps:
            available_slots.append(current_start)
        current_start += slot_interval
    return available_slots
