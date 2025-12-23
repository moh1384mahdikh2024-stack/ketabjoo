from django.db import models
from django.contrib.auth import get_user_model
from core.models import Book

User = get_user_model()
# Create your models here.

class Favorite(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="favorites", verbose_name="کاربر")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="favorites",
                             verbose_name="کتاب مورد علاقه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت", blank=True)

    def __str__(self):
        return f"{self.user} - book {self.book}"

    class Meta:
        verbose_name = "علاقه مندی"
        verbose_name_plural = "علاقه مندی"