from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
    RoleName = models.CharField(max_length=100, unique=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.RoleName

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    FullName = models.CharField(max_length=100)
    Gender = models.CharField(max_length=10)
    Role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.FullName

# Create your models here.
