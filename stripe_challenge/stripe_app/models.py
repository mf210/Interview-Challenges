from django.db import models



class Event(models.Model):
    event_type = models.CharField(max_length=250)
    event_id = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
