from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from encrypted_model_fields.fields import EncryptedIntegerField

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser):
    
    email =  models.EmailField(unique=True)

    class Meta:
        verbose_name_plural = 'Users'

    def clean_username(self, username):
        if CustomUser.objects.filter(username=self.username).exists():
            raise ValidationError('Username already exists')
        return username


class Category(TimestampModel):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Product(TimestampModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = EncryptedIntegerField() 
    category = models.ForeignKey(Category, on_delete= models.CASCADE)