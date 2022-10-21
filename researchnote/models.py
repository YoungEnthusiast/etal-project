from datetime import datetime
from django.db import models
from account.models import Researcher, Collab

class Note(models.Model):
    user = models.ForeignKey(Researcher, on_delete=models.CASCADE, related_name="research_note")
    collab = models.ForeignKey(Collab, null=True, blank=True, on_delete=models.SET_NULL, related_name="collab_research_note")
    title = models.CharField(max_length=200, verbose_name="")
    aims = models.CharField(max_length=255, verbose_name="")
    date_conducted = models.DateTimeField(null=True, blank=True, verbose_name="")
    location = models.CharField(max_length=200, null=True, blank=True, verbose_name="")
    setup = models.CharField(max_length=255,  null=True, blank=True, verbose_name="")
    method = models.TextField(null=True, blank=True, verbose_name="")
    result = models.TextField(null=True, blank=True, verbose_name="")
    observations = models.TextField(null=True, blank=True, verbose_name="")
    document = models.FileField(upload_to='research_notes/', null=True, blank=True, verbose_name="File")
    is_pinned = models.BooleanField(max_length=5, null=True, blank=True, default = False)
    serial = models.CharField(max_length=4, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        try:
            return str(self.content)
        except:
            return str(self.id)
