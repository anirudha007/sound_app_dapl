from django.db import models

# Create your models here.
class MyModel(models.Model):
        name = models.CharField(max_length=100)
        description = models.TextField()

        def __str__(self):
            return self.name
        
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    unique_string = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.unique_string