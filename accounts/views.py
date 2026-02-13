import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import MyUser
from reviews.models import Comment
from core.forms import CategoryForm, BookForm, AuthorForm
from core.models import Category, Book, Author
from invoices.models import InvoiceItem,Invoice


# Create your views here.
class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class NotLoginMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated


class RegisterView(NotLoginMixin, View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "accounts/register.html", {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            phone = data.get('phone')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            user = MyUser.objects.create_user(username=username, email=email, password=password, first_name=first_name,
                                              last_name=last_name)
            user.save()
            messages.success(request, "ثبت نام شما با موفقیت انجام شد لطفا وارد شوید")
            return redirect("login")
        return render(request, "accounts/register.html", {'form': form})


class LoginView(NotLoginMixin, View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print("h")
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید')
                return redirect("dashboard")
            messages.error(request, "نام کاربری یا گذرواژه شما اشتباه میباشد")
            return redirect("login")
        messages.error(request, "مشکلی پیش امده")
        return redirect("login")


class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            messages.success(request, "با موفقیت خارج شدید")
            return redirect("login")
        except:
            return redirect("home")


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_staff:
            return render(request, "accounts/admin_dashboard.html")
        return render(request, 'accounts/base_dashboard.html')


class NewCategoryView(StaffRequiredMixin, View):
    def get(self, request):
        category = Category.objects.all()
        return render(request, "accounts/category.html",
                      {"form": CategoryForm(), "cat": category, "is_child": False, "edit": False})


class UpdateCategoryView(StaffRequiredMixin, View):
    def get(self, request, cat_slug):
        category = Category.objects.get(slug=cat_slug)
        form = CategoryForm(instance=category)
        cat = Category.objects.all()
        return render(request, "accounts/category.html", {"form": form, "cat": cat, "is_child": True, "edit": True})


class NewAuthorView(StaffRequiredMixin, View):
    def get(self, request):
        form = AuthorForm()
        authors = Author.objects.all()
        return render(request, "accounts/author.html", {"form": form, "authors": authors, "edit": False})


class UpdateAuthorView(StaffRequiredMixin, View):
    def get(self, request, author_slug):
        author = get_object_or_404(Author, slug=author_slug)
        form = AuthorForm(instance=author)
        authors = Author.objects.all()
        return render(request, "accounts/author.html", {"form": form, "authors": authors, "edit": True})


class NewBookView(StaffRequiredMixin, View):
    def get(self, request):
        books = Book.objects.all().order_by("-created_at")[:4]
        form = BookForm()
        return render(request, "accounts/book.html", {"form": form, "books": books, "edit": False})


class UpdateBookView(StaffRequiredMixin, View):
    def get(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        form = BookForm(instance=book)
        books = Book.objects.all().order_by("-created_at")[:4]
        return render(request, "accounts/book.html", {"form": form, "books": books, "edit": True})


class CommentView(StaffRequiredMixin, View):
    def get(self, request):
        comments = Comment.objects.filter(status=Comment.Status.pending).order_by("-created_at")
        return render(request, "accounts/reviews_admin.html", {"reviews": comments})


class CartView(View):
    def get(self, request):
        cart = request.COOKIES.get("cart")
        books = []
        book_ids = []
        price = 0
        if cart:
            cart = json.loads(cart)
            for pk in cart:
                try:
                    book = Book.objects.get(pk=pk)
                    is_bought = InvoiceItem.objects.filter(book=book, invoice__user=request.user).exists()
                    if not is_bought:
                        books.append(book)
                        book_ids.append(book.pk)
                        price += book.price
                    else:
                        del cart[str(pk)]
                except:
                    del cart[str(pk)]
        else:
            cart = {}
        json_ids = json.dumps(book_ids)
        response = render(request, "accounts/cart.html",
                          context={"books": books, "json_ids":json_ids,"price": price, "addon_price": price * 10 / 100,
                                   "total_price": price + price * 10 / 100})
        response.set_cookie("cart", json.dumps(cart), max_age=24 * 60 * 60)
        return response


class AddCartView(View):
    def get(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        is_bought = InvoiceItem.objects.filter(book=book,invoice__user=request.user).exists()
        if not is_bought:
            cart = request.COOKIES.get("cart")
            if cart:
                cart = json.loads(cart)
            else:
                cart = {}
            if str(book.pk) in cart:
                messages.warning(request, "این کتاب از قبل در سبد خرید شما وجود دارد")
            else:
                cart[str(book.pk)] = book.pk
                messages.success(request, "به سبد خرید اضافه شد")
            response = redirect("book_detail", book_slug)
            response.set_cookie("cart", json.dumps(cart), max_age=24 * 60 * 60)
            return response
        else:
            messages.warning(request,"شما قبلا این کتاب را خریداری کرده اید")
            redirect("book_detail", book_slug)


class DeleteCartView(View):
    def get(self, request, book_slug):
        book = get_object_or_404(Book, slug=book_slug)
        cart = request.COOKIES.get("cart")
        if cart:
            cart = json.loads(cart)
            if str(book.pk) in cart:
                del cart[str(book.pk)]
                messages.success(request, "کتاب با موفقیت از سبد خرید پاک شد")
        response = redirect("cart")
        response.set_cookie("cart", json.dumps(cart), max_age=24 * 60 * 60)
        return response

class BoughtBookView(LoginRequiredMixin,View):
    def get(self, request):
        invoice_items = InvoiceItem.objects.filter(invoice__user=request.user)
        books = [i.book for i in invoice_items]
        for book in books:
            book.summary = book.summary[:60] + "..."
        return render(request,"accounts/bought_books.html" ,context={"books":books})

