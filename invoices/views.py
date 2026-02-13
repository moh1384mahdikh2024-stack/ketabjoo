from django.shortcuts import render
from .models import Invoice,User,InvoiceItem
from core.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import json

# Create your views here.

class AddInvoiceView(LoginRequiredMixin, View):
    def post(self, request):
        books = request.POST.get("books")
        price = int(request.POST.get("price"))
        books = json.loads(books)
        invoice=Invoice.objects.create(user=request.user, price=price)
        cart = request.COOKIES.get("cart")
        cart = json.loads(cart)
        for book_id in books:
            book = Book.objects.get(pk=book_id)
            InvoiceItem.objects.create(book=book, invoice=invoice)
            del cart[str(book_id)]

        response = redirect("mybook")
        response.set_cookie("cart", cart)
        return response



