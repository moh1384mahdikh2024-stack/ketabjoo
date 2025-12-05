from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    phone = models.CharField(max_length=15, unique=True,verbose_name="شماره تلفن")
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True,
                                        default='profile_pictures/default.jpg',verbose_name="عکس پروفایل")

    def __str__(self):
        return (self.first_name + ' ' + self.last_name) if self.first_name and self.last_name else self.username

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر"