from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Comment
from core.models import Book
from statistics import mean

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff
# Create your views here.

class CommentsView(View):
    def post(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        score = request.POST.get("rating")
        content = request.POST.get("comment")
        new_comment = Comment.objects.create(content=content, score=score,book=book,author=request.user)
        messages.success(request,"نظر شما با موفقیت ثبت و پس از بررسی در قسمت نظرات قرار خواهد گرفت")
        return redirect("book_detail", book_slug)

class AcceptCommentsView(StaffRequiredMixin,View):
    def get(self, request, review_id):
        comment = get_object_or_404(Comment, pk=review_id)
        comment.status=Comment.Status.accepted
        comment.save()
        messages.success(request,"کامنت پذیرفته شد")
        return redirect("status_comment_admin")
class RejectCommentsView(StaffRequiredMixin,View):
    def get(self, request, review_id):
        comment = get_object_or_404(Comment, pk=review_id)
        comment.status=Comment.Status.rejected
        comment.save()
        messages.warning(request,"کامنت رد شد")
        return redirect("status_comment_admin")