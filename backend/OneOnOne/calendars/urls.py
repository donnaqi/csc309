from django.urls import path
from calendars.views.create_calendar import CalendarCreationView
from calendars.views.update_calendar import CalendarUpdateView
from calendars.views.view_calendar import CalendarView
from .views.suggested_view import CalendarEventSuggestedView, FinalizeScheduleView
from calendars.views.event_views import EventAllListView, EventCreationView, EventReminderView, EventUpdateView

app_name = 'calendar'
urlpatterns = [
    path('create/', CalendarCreationView.as_view(), name='create_calendar'),
    path('update/', CalendarUpdateView.as_view(), name='update_calendar'),
    path('view/<int:yr>/<int:wk>/', CalendarView.as_view(), name='view_calendar'),
    path('view/<int:event_id>/suggested_schedule',CalendarEventSuggestedView.as_view(), name='suggested_schedule'),
    path('view/<int:event_id>/finalize_schedule',FinalizeScheduleView.as_view(), name='finalize_schedule'),

    # Events Urls

    path('event/add', EventCreationView.as_view(), name='create_event'),
    path('event/<int:pk>/edit', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:event_id>/remind', EventReminderView.as_view(), name='event_remind'),
    path('event/list', EventAllListView.as_view(), name='all_event'),
]
