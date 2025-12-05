from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=250, verbose_name="نام کتاب")
    author = models.CharField(max_length=250, verbose_name="نویسنده")
    summary = models.TextField("خلاصه")
    price = models.DecimalField(verbose_name="قیمت", max_digits=10, decimal_places=0)
    discount = models.PositiveSmallIntegerField("تخفیف", validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                blank=True, default=0)
    publisher = models.CharField(max_length=250, verbose_name="ناشر")
    translator = models.CharField(max_length=250, verbose_name="مترجم", null=True, blank=True)
    thumbnail = models.ImageField(upload_to="thumbnails", default="thumbnails/default.jpg", verbose_name="عکس اصلی")
    pdf_file = models.FileField(upload_to="pdf", verbose_name="فایل pdf")
    category = models.ForeignKey(to="Category", on_delete=models.CASCADE, related_name="books",
                                 verbose_name="دسته بندی")
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="امتیاز", default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "کتاب"
        verbose_name_plural = "کتاب"


class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name="نام دسته")
    description = models.TextField("توضیحات دسته")
    thumbnail = models.ImageField("عکس دسته", upload_to="cat_thumbnails", default="cat_thumbnails/default.jpg",
                                  blank=True)
    parent = models.ForeignKey(to="Category", verbose_name="دسته مادر", on_delete=models.CASCADE,
                               related_name="children")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی"


# class Comment(models.Model):
#     author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="comments", verbose_name="نویسنده نظر")
#     book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="comments", verbose_name="کتاب")
#     content = models.TextField("محتوای نظر")
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="تاریخ کامنت")
#     score = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
#                                              verbose_name="امتیاز", default=1)
#     reply = models.ForeignKey(to='self', on_delete=models.CASCADE, related_name="replies", verbose_name="پاسخ به",
#                               null=True, blank=True)
#
#     def __str__(self):
#         return self.content
#
#     class Meta:
#         verbose_name = "نظر"
#         verbose_name_plural = "نظر"


# class Favorite(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="favorites", verbose_name="کاربر")
#     book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="favorites",
#                              verbose_name="کتاب مورد علاقه")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت", blank=True)
#
#     def __str__(self):
#         return f"{self.user} - book {self.book}"
#
#     class Meta:
#         verbose_name = "علاقه مندی"
#         verbose_name_plural = "علاقه مندی"

# class InvoiceBook(models.Model):
#     invoice = models.ForeignKey(to="Invoice", on_delete=models.CASCADE, related_name="invoice_books",
#                                 verbose_name="فاکتور")
#     book = models.ForeignKey(to=Book, on_delete=models.CASCADE, related_name="invoice",
#                              verbose_name="کتاب خریداری شده")
#     purchase_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ فروش", blank=True)
#     price = models.DecimalField(verbose_name="قیمت هنگام فروش", max_digits=10, decimal_places=0)
#
#     def __str__(self):
#         return f"{self.book.title} - Invoice {self.invoice.tracking_code}"
#
#     class Meta:
#         verbose_name = "رابطه کتاب و فاکتور"
#         verbose_name_plural = "رابطه کتاب و فاکتور"
#
#
# class Invoice(models.Model):
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name="invoice", verbose_name="خریدار")
#     total_price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="قیمت کل")
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ فاکتور")
#     tracking_code = models.CharField(max_length=16, verbose_name="کد رهگیری")
#     coupon = models.ForeignKey(to="Coupon", on_delete=models.SET_NULL, related_name="invoice_coupon",
#                                verbose_name="کد تخفیف", null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.user} - Invoice {self.tracking_code}"
#
#     class Meta:
#         verbose_name = "فاکتور فروش"
#         verbose_name_plural = "فاکتور فروش"
#
#
# class Coupon(models.Model):
#     coupon = models.CharField(max_length=25, verbose_name="کد تخفیف")
#     percent = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
#                                           verbose_name="درصد تخفیف")
#     is_active = models.BooleanField(default=False, verbose_name="فعال است؟")
#
#     def __str__(self):
#         return self.coupon
#
#     class Meta:
#         verbose_name = "تخفیف"
#         verbose_name_plural = "تخفیف"
