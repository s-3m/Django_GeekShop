from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.
class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatar', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18, null=True)
    city = models.CharField(verbose_name='Город', max_length=36, blank=True)

    activation_key = models.CharField(verbose_name='Код активации', max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(verbose_name='Истечение срока активации', default=(now() + timedelta(hours=48)))


    def is_activation_key_expires(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
