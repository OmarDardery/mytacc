from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=15, blank=False, unique=True, error_messages={"unique": "This ID has already been used.", 'blank': "This field cannot be blank."}, validators=[MaxLengthValidator(15), MinLengthValidator(8)])
    email = models.EmailField(unique=True, error_messages={'unique': "This email address is already in use.", 'blank': "This field cannot be blank."})
    password = models.CharField(max_length=15, blank=False, validators=[MaxLengthValidator(15), MinLengthValidator(8)])
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
