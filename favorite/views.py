from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View
from .models import Favorite
from core.models import Book
# Create your views here.

class AddFavorite(LoginRequiredMixin,View):
    def get(self, request,book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        new_favorite = Favorite.objects.create(user=request.user, book=book)
        messages.success(request,"کتاب به علاقه مندی های شما افزوده شد")
        return redirect("book_detail",book_slug=book_slug)

class RemoveFavorite(LoginRequiredMixin,View):
    def get(self, request,book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        favorite = get_object_or_404(Favorite, user=request.user, book=book)
        favorite.delete()
        messages.warning(request,"کتاب از لیست علاقه مندی های شما خارج شد")
        return redirect("book_detail",book_slug=book_slug)
