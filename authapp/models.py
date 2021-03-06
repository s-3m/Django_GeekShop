from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class ShopUserProfile(models.Model):
    male = "M"
    female = "F"

    gender_choices = (
        (male, 'Male'),
        (female, 'Fimale')
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, blank=True)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=gender_choices, blank=True)
    domain = models.CharField(verbose_name='ссылка на профиль', max_length=256, blank=True)
    faw_music = models.CharField(verbose_name='любимая музыка', max_length=1000, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
