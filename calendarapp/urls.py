from django.urls import path

from . import views

app_name = "calendarapp"


urlpatterns = [
    # path("calender/", views.CalendarViewNew.as_view(), name="calendar"),
    path('collab/view-initiated/<str:id1>/schedules/', views.CalendarViewNew.as_view(), name="schedules-initiated"),
    path('collab/view-initiated/<str:id1>/all-schedules/', views.showAllEventsInitiated, name="all-schedules-initiated"),
    path('collab/view-initiated/<str:id1>/all-schedules/select/<str:id2>', views.selectEventInitiated, name='update_event_initiated'),
    path('collab/view-initiated/<str:id1>/all-schedules/deselect/<str:id2>', views.deselectEventInitiated, name='deselect_event_initiated'),
    path('collab/view-initiated/<str:id1>/all-schedules/delete-all', views.deleteAllEventsInitiated, name='delete_all_events_initiated'),

    path('collab/view-initiated/schedules/<str:id1>/<str:id2>', views.showEventInitiated, name='show_event_initiated'),

    path('collab/view-initiated/schedules/<str:id1>/<str:id2>', views.showEventInitiated2, name='show_event_initiated2'),


    path('collab/view-initiated/schedules/<str:id1>/<str:id2>/update', views.updateEventInitiated, name='update_event_initiated'),
    path('collab/view-initiated/schedules/<str:id1>/<str:id2>/delete', views.deleteEventInitiated, name='delete_event_initiated'),

    path("collab/view-initiated/schedule/<str:id1>", views.create_event, name="event_new"),

    path("calenders/", views.CalendarView.as_view(), name="calendars"),

    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path(
        "add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"
    ),
    path(
        "event/<int:pk>/remove",
        views.EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
]
