from datetime import datetime
from django.db import models
from django.urls import reverse
from calendarapp.models import EventAbstract
from account.models import Researcher, Collab
from django.utils import timezone

class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

class EventAvailable(models.Model):
    AVAILABLE_CHOICES = [
        ('Yes','Yes'),
        ('No', 'No'),
        ('Maybe', 'Maybe')
    ]
    available = models.CharField(max_length=5, choices=AVAILABLE_CHOICES, default='Maybe', null=True)
    creator = models.ForeignKey(Researcher, null=True, blank=True, on_delete=models.SET_NULL, related_name="event_creator")
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.available)
        except:
            return str(self.id)

class Event(EventAbstract):
    """ Event model """
    user = models.ForeignKey(Researcher, on_delete=models.CASCADE, related_name="events")
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_scheduler")
    title = models.CharField(max_length=200, verbose_name="")
    available_choice = models.ManyToManyField(EventAvailable, blank=True, verbose_name="Available", related_name="update_text")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Ending Time")
    location = models.CharField(max_length=200, null=True, blank=True, verbose_name="")
    link = models.CharField(max_length=200,  null=True, blank=True, verbose_name="")
    description = models.TextField(null=True, blank=True, verbose_name="")
    is_selected = models.ManyToManyField(Researcher, blank=True, related_name="is_selected_event")
    start_time = models.DateTimeField(null=True, blank=True, verbose_name="Starting Time")
    reminder = models.DateTimeField(blank=True, null= True)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
