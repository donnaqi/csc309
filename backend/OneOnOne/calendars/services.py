from collections import defaultdict
from calendars.models.event import Event
from calendars.models.timeblock import TimeBlock
from calendars.models.calendar import Calendar


def suggest_schedules(event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return []

    participants = event.participants.all()
    participants = list(participants)
    if event.owner not in participants:
        participants.append(event.owner)
    print(participants)
    event_date = event.date.date()
    event_duration_blocks = event.duration // 30

    # availability is a dictionary with time slots as keys and a dictionary as values,
    # inside the dictionary, 'count' is the number of participants available at that time, 'score' is the sum of their preferences
    # e.g.:
    # {12.5: {'count': 1, 'score': 1}, 12.0: {'count': 2, 'score': 2}, ...}
    availability = defaultdict(lambda: {'count': 0, 'score': 0})
    unavailable_participants = []

    for participant in participants:
        calendar = Calendar.objects.filter(owner=participant).first()
        if calendar:
            time_blocks = TimeBlock.objects.filter(
                calendar=calendar,
                yr=event_date.year,
                wk=event_date.isocalendar()[1],
                day=event_date.isocalendar()[2],
            )

            if not time_blocks.exists():
                unavailable_participants.append(participant)
                continue

            for block in time_blocks:
                if block.preference is not None:
                    availability[block.time]['count'] += 1
                    availability[block.time]['score'] += block.preference

    # Filter for slots where all participants are available
    # all_available_slots is a list of all avaliable time slots, e.g. [12.0, 12.5, ...]
    all_available_slots = [
        time for time, info in availability.items()
        if info['count'] == len(participants)
    ]

    # Sort slots by total preference score, then by time
    all_available_slots.sort(key=lambda x: (availability[x]['score'], x))

    # Now find contiguous time slots that match the event duration
    suggested_schedules = []
    for i in range(len(all_available_slots)):
        start_time = all_available_slots[i]
        if all(
            (start_time + 0.5*j) in all_available_slots
            for j in range(event_duration_blocks)
        ):
            end_time = start_time + 0.5 * event_duration_blocks
            schedule = {"date": event_date, "yr": event_date.year, "wk": event_date.isocalendar(
            )[1], "day": event_date.isocalendar()[2], "start_time": start_time, "end_time": end_time}
            suggested_schedules.append(schedule)

    return suggested_schedules
