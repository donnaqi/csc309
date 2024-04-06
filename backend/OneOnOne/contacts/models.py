from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_contact = models.CharField(max_length=20)
    pronoun = models.CharField(max_length=20, null=True, blank=True)
    tag_line = models.CharField(max_length=50, null=True, blank=True)
    accessibility = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def email(self):
        return self.user.email