from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import CategoryForm, BookForm, AuthorForm
from .models import Category, Book, Author
from reviews.models import Comment
from favorite.models import Favorite


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


# Create your views here.

def home(request):
    books = Book.objects.filter(is_deleted=False)
    for book in books:
        book.summary = book.summary[:60] + "..."
    return render(request, "core/index.html", {"books": books})


class CreateCategory(StaffRequiredMixin, View):
    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "دسته جدید ساخته شد")
            return redirect("category_admin")
        messages.error(request, "مقادیر وارد شده دارای مشکل است لطفا دوباره تلاش کنید")
        return redirect("category_admin")


class UpdateCategory(StaffRequiredMixin, View):
    def post(self, request, cat_slug):
        parts = cat_slug.strip("/").split("/")
        category = None
        parent = None
        for slug in parts:
            cat = get_object_or_404(Category, slug=slug, parent=parent)
            # category = Category.objects.get(slug=slug, parent=parent)
            parent = category  # برای مرحله بعد
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "دسته با موفقیت ویرایش شد")
            return redirect("category_admin")
        messages.error(request, "مقادیر وارد شده دارای مشکل است لطفا دوباره تلاش کنید")
        return redirect("update_category_admin", cat_slug)


class CreateAuthor(StaffRequiredMixin, View):
    def post(self, request):
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "نویسنده جدید افوزده شد")
            return redirect("author_admin")
        messages.error(request, "مقادیر وارد شده دارای مشکل است لطفا دوباره تلاش کنید")
        return redirect("author_admin")


class UpdateAuthor(StaffRequiredMixin, View):
    def post(self, request, author_slug):
        author = get_object_or_404(Author, slug=author_slug)
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "نویسنده با موفقیت ویرایش شد")
            return redirect("author_admin")
        messages.error(request, "مقادیر وارد شده دارای مشکل است لطفا دوباره تلاش کنید")
        return redirect("update_author_admin", author_slug)


class CreateBook(StaffRequiredMixin, View):
    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            b = form.save(commit=False)
            b.save()
            form.save_m2m()
            messages.success(request, "کتاب جدید ساخته شد")
            return redirect("book_admin")
        messages.error(request, "مقادیر وارد شده دارای مشکل است لطفا دوباره تلاش کنید")
        return redirect("book_admin")


class UpdateBook(StaffRequiredMixin, View):
    def post(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            b = form.save(commit=False)
            b.save()
            form.save_m2m()
            messages.success(request, "کتاب با موفقیت ویرایش شد")
            return redirect("book_admin")
        messages.error(request, "مقادیر وارد شده دارای مشکل است لطفا دوباره تلاش کنید")
        return redirect("update_book_admin", book_slug)


class DeleteBook(StaffRequiredMixin, View):
    def get(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        book.is_deleted = True
        book.save()
        messages.success(request, "کتاب با موفقیت پاک شد")
        return redirect("book_admin")


class BookDetailView(View):
    def get(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        comments = Comment.objects.filter(book=book, reply=None, status="a")
        is_favor = Favorite.objects.filter(user=request.user, book=book).exists()
        return render(request, "core/book_detail.html", {"book": book, "comments": comments, "is_favor": is_favor})
