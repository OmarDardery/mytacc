from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=15, blank=False, unique=True, error_messages={"unique": "This ID has already been used.", 'blank': "This field cannot be blank."}, validators=[MaxLengthValidator(15), MinLengthValidator(8)])
    email = models.EmailField(unique=True, error_messages={'unique': "This email address is already in use.", 'blank': "This field cannot be blank."})
    password = models.CharField(max_length=15, blank=False, validators=[MaxLengthValidator(15), MinLengthValidator(8)])
    points = models.IntegerField(default=0)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="No name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    completed = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Debt(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(default="No name")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debts')
    points = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)