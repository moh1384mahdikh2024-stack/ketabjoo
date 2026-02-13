from django.db import models
from core.models import Book
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Invoice(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="invoices")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "پرداختی"
        verbose_name_plural = "پرداختی"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.pk}"


class InvoiceItem(models.Model):
    objects = models.Manager()
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name="invoice_items")
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE,related_name="invoice_items")
    class Meta:
        verbose_name = "کتاب خریده شده"
        verbose_name_plural = "کتاب خریده شده"
    def __str__(self):
        return f"{self.invoice} : {self.book}"

