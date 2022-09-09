from django.db import models
from authentication.models import User
from helpers.models import TrackingModel

class Todo(TrackingModel):
    title = models.CharField(max_length=30)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
