from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Calendar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Calendar owned by {self.owner}"