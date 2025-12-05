from django.shortcuts import render, redirect
# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import LoginForm,RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import MyUser

# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request,"accounts/register.html",{'form':form})

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
            user = MyUser.objects.create_user(username=username,email=email,password=password,first_name=first_name,last_name=last_name)
            user.save()
            messages.success(request,"ثبت نام شما با موفقیت انجام شد لطفا وارد شوید")
            return redirect("login")
        return render(request,"accounts/register.html",{'form':form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username,password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                print("h")
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید')
                return redirect("dashboard")
            messages.error(request,"نام کاربری یا گذرواژه شما اشتباه میباشد")
            return redirect("login")
        messages.error(request,"مشکلی پیش امده")
        return redirect("login")



class LogoutView(View):
    def get(self, request):
        try:
            logout(request)
            messages.success(request,"با موفقیت خارج شدید")
            return redirect("login")
        except:
            return redirect("home")


class DashboardView(LoginRequiredMixin,View):
    def get(self, request):
        if request.user.is_staff:
            return render(request,"accounts/admin_dashboard.html")
        return render(request, 'accounts/base_dashboard.html')

