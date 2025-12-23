from django.core.validators import MinValueValidator,MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model
from core.models import Book

User = get_user_model()

# Create your models here.


class Comment(models.Model):
    class Status(models.TextChoices):
        accepted =("a","پذیرفته شده")
        rejected =("r","رد شده")
        pending =("p","در حال بررسی")
    objects = models.Manager()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", verbose_name="نویسنده نظر")
    book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="comments", verbose_name="کتاب")
    content = models.TextField("محتوای نظر")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="تاریخ کامنت")
    score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                             verbose_name="امتیاز", default=1)
    reply = models.ForeignKey(to='self', on_delete=models.CASCADE, related_name="replies", verbose_name="پاسخ به",
                              null=True, blank=True)
    status = models.CharField(max_length=3,blank=True,choices=Status.choices,default=Status.pending,verbose_name="وضعیت")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظر"

