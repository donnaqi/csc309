from django.db import models
from django.contrib.auth.models import User
from contacts.models import Contact


class Event(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_events')
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    date = models.DateTimeField()
    start_time = models.TimeField(null=True, blank=True)
    duration = models.IntegerField(default=30)
    participants = models.ManyToManyField(
        User, related_name='events', blank=True)
    last_modified = models.DateTimeField(auto_now=True)
    '''   Invite = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_invites', null=True, blank=True)
    Receive = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='received_invites', null=True, blank=True)'''

    def __str__(self):
        return self.name
